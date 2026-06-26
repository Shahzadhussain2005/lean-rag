import { useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { CloudUpload, FileText } from "lucide-react";
import { clsx } from "clsx";
import { Spinner } from "@/components/ui/Spinner";

const ACCEPTED_TYPES = {
  "application/pdf": [".pdf"],
  "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"],
  "text/plain": [".txt"],
  "text/markdown": [".md"],
};

interface UploadZoneProps {
  onUpload: (file: File) => Promise<unknown>;
  isUploading: boolean;
}

export function UploadZone({ onUpload, isUploading }: UploadZoneProps) {
  const onDrop = useCallback(
    (accepted: File[]) => {
      if (accepted[0]) onUpload(accepted[0]);
    },
    [onUpload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: ACCEPTED_TYPES,
    maxFiles: 1,
    disabled: isUploading,
    maxSize: 20 * 1024 * 1024,
  });

  return (
    <div
      {...getRootProps()}
      className={clsx(
        "flex flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-8 cursor-pointer transition-colors",
        isDragActive
          ? "border-brand-500 bg-brand-500/5"
          : "border-gray-700 hover:border-gray-600 hover:bg-gray-800/50",
        isUploading && "opacity-60 cursor-not-allowed"
      )}
    >
      <input {...getInputProps()} />
      {isUploading ? (
        <Spinner size="lg" />
      ) : (
        <div className="flex h-12 w-12 items-center justify-center rounded-full bg-gray-800">
          {isDragActive ? (
            <CloudUpload className="h-6 w-6 text-brand-400" />
          ) : (
            <FileText className="h-6 w-6 text-gray-400" />
          )}
        </div>
      )}
      <div className="text-center">
        <p className="text-sm font-medium text-gray-300">
          {isUploading ? "Uploading & processing…" : isDragActive ? "Drop it here" : "Upload a document"}
        </p>
        <p className="mt-1 text-xs text-gray-500">PDF, DOCX, TXT, MD · up to 20 MB</p>
      </div>
    </div>
  );
}
