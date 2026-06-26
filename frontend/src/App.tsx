import { Sidebar } from "@/components/layout/Sidebar";
import { ChatPanel } from "@/components/features/ChatPanel";

export default function App() {
  return (
    <div className="flex h-screen overflow-hidden bg-gray-950">
      <Sidebar />
      <main className="flex-1 overflow-hidden">
        <ChatPanel />
      </main>
    </div>
  );
}
