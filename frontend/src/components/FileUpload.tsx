"use client";

import { useState } from "react";
import { Upload, CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function FileUpload({ 
  onUploadSuccess, 
  sessionId 
}: { 
  onUploadSuccess: (id: string, files: string[]) => void,
  sessionId: string | null
}) {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files?.length) return;
    
    setUploading(true);
    setError(null);
    
    const formData = new FormData();
    Array.from(e.target.files).forEach(file => {
      formData.append("files", file);
    });
    
    const url = sessionId 
      ? `http://localhost:8000/upload?session_id=${sessionId}` 
      : "http://localhost:8000/upload";

    try {
      const res = await fetch(url, {
        method: "POST",
        body: formData,
      });
      
      if (!res.ok) throw new Error("Upload failed");
      
      const data = await res.json();
      onUploadSuccess(data.session_id, data.filenames);
    } catch (err) {
      setError("Failed to upload files. Please try again.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-lg border border-gray-200">
      <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50 transition-colors">
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          {uploading ? (
            <Loader2 className="w-8 h-8 text-blue-500 animate-spin" />
          ) : (
            <Upload className="w-8 h-8 text-gray-400 mb-2" />
          )}
          <p className="text-sm text-gray-500">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-gray-400">PDF files only</p>
        </div>
        <input 
          type="file" 
          className="hidden" 
          multiple 
          accept=".pdf" 
          onChange={handleFileChange}
          disabled={uploading}
        />
      </label>
      
      {error && (
        <div className="mt-4 flex items-center text-red-500 text-xs">
          <AlertCircle className="w-4 h-4 mr-1" />
          {error}
        </div>
      )}
      
      {sessionId && !uploading && !error && (
        <div className="mt-4 flex items-center text-green-600 text-xs">
          <CheckCircle className="w-4 h-4 mr-1" />
          Ready to chat!
        </div>
      )}
    </div>
  );
}
