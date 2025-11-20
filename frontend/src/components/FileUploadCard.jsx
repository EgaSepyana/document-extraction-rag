import { useRef, useState } from "react";
import {
  Upload,
  Send,
  File,
  X,
  MessageSquare,
  AlertCircle,
  Plus,
  Trash2,
  Menu,
  XCircle,
} from "lucide-react";

const FileUploadCard = ({ onFileSelect, uploadedFile, onRemoveFile }) => {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handledrag = (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === "dragenter" || e.type == "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const hadlerDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file) => {
    const validTypes = [
      "application/pdf",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
      "application/msword",
      "text/csv",
    ];

    if (validTypes.includes(file.type)) {
      onFileSelect(file);
    } else {
      alert("Please upload a valid file (PDF, DOCX, DOC, or CSV)");
    }
  };

  return (
    <div
      className={`border-3 border-dashed rounded-xl px-6 py-12 text-center transition-all ${
        dragActive
          ? "border-blue-500"
          : "border-primary-border dark:border-primary-border-dark"
      }`}
      onDragEnter={handledrag}
      onDragLeave={handledrag}
      onDragOver={handledrag}
      onDrop={hadlerDrop}
    >
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.doc,.docx,.csv"
        onChange={handleFileInput}
      />
      <Upload className="w-12 h-12 mx-auto mb-3 dark:text-icon-dark-secondary" />
      <p className="text-2xl font-semibold text-gray-700 mb-2">
        Upload a file to start
      </p>
      <p className="text-lg font-semibold text-gray-700 mb-4">
        Drag & drop files here
      </p>
      <button
        onClick={() => fileInputRef.current.click()}
        className="cursor-pointer text-lg text-neutral-200 dark:bg-button-bg-primary mb-4 px-6 py-3 rounded-lg transition-colors"
      >
        Or Browser File
      </button>
      <p className="text-font-secondary text-lg">
        Supported: PDF, DOCX, DOC, CSV
      </p>
    </div>
  );
};

export default FileUploadCard;
