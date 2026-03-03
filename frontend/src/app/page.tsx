"use client";

import { useState } from "react";
import FileUpload from "@/components/FileUpload";
import Chat from "@/components/Chat";

export default function Home() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [files, setFiles] = useState<string[]>([]);

  const handleUploadSuccess = (id: string, uploadedFiles: string[]) => {
    setSessionId(id);
    setFiles((prev) => [...new Set([...prev, ...uploadedFiles])]);
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-8 bg-gray-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm flex flex-col gap-8">
        <h1 className="text-4xl font-bold text-blue-600">DocuChat AI</h1>
        
        <div className="w-full grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="md:col-span-1 space-y-6">
            <FileUpload onUploadSuccess={handleUploadSuccess} sessionId={sessionId} />
            {files.length > 0 && (
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="font-bold mb-2">Uploaded Documents</h3>
                <ul className="list-disc pl-4 text-xs space-y-1">
                  {files.map((f, i) => (
                    <li key={i} className="truncate">{f}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
          
          <div className="md:col-span-2">
            <Chat sessionId={sessionId} />
          </div>
        </div>
      </div>
    </main>
  );
}
