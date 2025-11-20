import React, { useState, useRef, useEffect } from "react";
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

// API Configuration
const API_CONFIG = {
  baseURL: "https://api.yourbackend.com",
  endpoints: {
    upload: "/api/upload",
    chat: "/api/chat",
    createChat: "/api/chat/create",
    deleteChat: "/api/chat/delete",
  },
};

// API Service
const apiService = {
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      `${API_CONFIG.baseURL}${API_CONFIG.endpoints.upload}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) throw new Error("Upload failed");
    return response.json();
  },

  sendMessage: async (message, chatId) => {
    const response = await fetch(
      `${API_CONFIG.baseURL}${API_CONFIG.endpoints.chat}`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message, chatId }),
      }
    );

    if (!response.ok) throw new Error("Message failed");
    return response.json();
  },
};

// Components
const Sidebar = ({
  chats,
  activeChat,
  onSelectChat,
  onNewChat,
  onDeleteChat,
  isMobileOpen,
  onCloseMobile,
}) => {
  return (
    <>
      {/* Mobile Overlay */}
      {isMobileOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onCloseMobile}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
        fixed lg:static inset-y-0 left-0 z-50
        w-80 bg-white border-r border-gray-200 flex flex-col
        transform transition-transform duration-300 ease-in-out
        ${isMobileOpen ? "translate-x-0" : "-translate-x-full lg:translate-x-0"}
      `}
      >
        {/* Sidebar Header */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-gray-800">
              Conversations
            </h2>
            <button
              onClick={onCloseMobile}
              className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <button
            onClick={onNewChat}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white px-4 py-3 rounded-lg font-medium transition-colors flex items-center justify-center space-x-2"
          >
            <Plus className="w-5 h-5" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Chat List */}
        <div className="flex-1 overflow-y-auto p-4 space-y-2">
          {chats.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <MessageSquare className="w-12 h-12 mx-auto mb-2 opacity-50" />
              <p className="text-sm">No conversations yet</p>
              <p className="text-xs mt-1">Create a new chat to start</p>
            </div>
          ) : (
            chats.map((chat) => (
              <div
                key={chat.id}
                className={`
                  group relative p-3 rounded-lg cursor-pointer transition-all
                  ${
                    activeChat?.id === chat.id
                      ? "bg-blue-50 border-2 border-blue-200"
                      : "bg-gray-50 hover:bg-gray-100 border-2 border-transparent"
                  }
                `}
                onClick={() => onSelectChat(chat.id)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center space-x-2 mb-1">
                      <File className="w-4 h-4 text-blue-600 shrink-0" />
                      <p className="text-sm font-semibold text-gray-800 truncate">
                        {chat.fileName || "Untitled Chat"}
                      </p>
                    </div>
                    <p className="text-xs text-gray-600 truncate">
                      {chat.messages.length} messages
                    </p>
                    <p className="text-xs text-gray-400 mt-1">
                      {chat.createdAt}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onDeleteChat(chat.id);
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1.5 hover:bg-red-100 rounded transition-opacity"
                  >
                    <Trash2 className="w-4 h-4 text-red-500" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </>
  );
};

const FileUploadCard = ({ onFileSelect, uploadedFile, onRemoveFile }) => {
  const fileInputRef = useRef(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
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

  if (uploadedFile) {
    return (
      <div className="bg-linear-to-r from-blue-50 to-indigo-50 border-2 border-blue-200 rounded-xl p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="bg-blue-500 p-2 rounded-lg">
              <File className="w-5 h-5 text-white" />
            </div>
            <div>
              <p className="font-semibold text-gray-800 text-sm">
                {uploadedFile.name}
              </p>
              <p className="text-xs text-gray-600">
                {(uploadedFile.size / 1024).toFixed(2)} KB
              </p>
            </div>
          </div>
          <button
            onClick={onRemoveFile}
            className="p-1.5 hover:bg-red-100 rounded-lg transition-colors"
          >
            <X className="w-4 h-4 text-red-500" />
          </button>
        </div>
      </div>
    );
  }

  return (
    <div
      className={`border-2 border-dashed rounded-xl p-6 text-center transition-all ${
        dragActive
          ? "border-blue-500 bg-blue-50"
          : "border-gray-300 bg-gray-50 hover:border-blue-400"
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        accept=".pdf,.doc,.docx,.csv"
        onChange={handleFileInput}
      />
      <Upload className="w-10 h-10 mx-auto mb-3 text-gray-400" />
      <p className="text-base font-semibold text-gray-700 mb-2">
        Upload a file to start
      </p>
      <p className="text-xs text-gray-500 mb-3">
        Drag and drop or click to browse
      </p>
      <button
        onClick={() => fileInputRef.current.click()}
        className="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-lg font-medium transition-colors text-sm"
      >
        Select File
      </button>
      <p className="text-xs text-gray-400 mt-3">
        Supported: PDF, DOCX, DOC, CSV
      </p>
    </div>
  );
};

const ChatMessage = ({ message, isUser }) => {
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} mb-4`}>
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-3 ${
          isUser ? "bg-blue-600 text-white" : "bg-gray-100 text-gray-800"
        }`}
      >
        <p className="text-sm whitespace-pre-wrap">{message.content}</p>
        <span className="text-xs opacity-70 mt-1 block">
          {message.timestamp}
        </span>
      </div>
    </div>
  );
};

const ChatInput = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState("");

  const handleSubmit = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input);
      setInput("");
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="border-t bg-white p-4">
      <div className="flex space-x-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={disabled}
          placeholder={
            disabled
              ? "Upload a file to start chatting..."
              : "Type your message..."
          }
          className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 disabledR:cursor-not-allowed text-white px-6 py-3 rounded-lg transition-colors flex items-center space-x-2"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

const EmptyState = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full text-center p-8">
      <div className="bg-blue-100 p-6 rounded-full mb-4">
        <MessageSquare className="w-12 h-12 text-blue-600" />
      </div>
      <h3 className="text-xl font-semibold text-gray-800 mb-2">
        Ready to Chat!
      </h3>
      <p className="text-gray-600">
        Start a conversation by typing your message below
      </p>
    </div>
  );
};

// Main App Component
const App = () => {
  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isMobileSidebarOpen, setIsMobileSidebarOpen] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [activeChat?.messages]);

  const createNewChat = () => {
    const newChat = {
      id: Date.now(),
      fileName: null,
      uploadedFile: null,
      messages: [],
      createdAt: new Date().toLocaleString(),
    };

    setChats((prev) => [newChat, ...prev]);
    setActiveChat(newChat);
    setIsMobileSidebarOpen(false);
  };

  const selectChat = (chatId) => {
    const chat = chats.find((c) => c.id === chatId);
    if (chat) {
      setActiveChat(chat);
      setIsMobileSidebarOpen(false);
    }
  };

  const deleteChat = (chatId) => {
    if (window.confirm("Are you sure you want to delete this conversation?")) {
      setChats((prev) => prev.filter((c) => c.id !== chatId));
      if (activeChat?.id === chatId) {
        setActiveChat(null);
      }
    }
  };

  const updateActiveChat = (updates) => {
    setChats((prev) =>
      prev.map((chat) =>
        chat.id === activeChat.id ? { ...chat, ...updates } : chat
      )
    );
    setActiveChat((prev) => ({ ...prev, ...updates }));
  };

  const handleFileSelect = async (file) => {
    if (!activeChat) return;

    try {
      // Replace with actual API call
      // const response = await apiService.uploadFile(file);

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const systemMessage = {
        id: Date.now(),
        content: `File "${file.name}" uploaded successfully! You can now start asking questions about the document.`,
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      updateActiveChat({
        uploadedFile: file,
        fileName: file.name,
        messages: [systemMessage],
      });
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to upload file. Please try again.");
    }
  };

  const handleRemoveFile = () => {
    if (
      window.confirm("Removing the file will clear all messages. Continue?")
    ) {
      updateActiveChat({
        uploadedFile: null,
        fileName: null,
        messages: [],
      });
    }
  };

  const handleSendMessage = async (messageContent) => {
    if (!activeChat) return;

    const userMessage = {
      id: Date.now(),
      content: messageContent,
      isUser: true,
      timestamp: new Date().toLocaleTimeString(),
    };

    updateActiveChat({
      messages: [...activeChat.messages, userMessage],
    });

    setIsLoading(true);

    try {
      // Replace with actual API call
      // const response = await apiService.sendMessage(messageContent, activeChat.id);

      await new Promise((resolve) => setTimeout(resolve, 1000));

      const aiMessage = {
        id: Date.now() + 1,
        content: `This is a simulated response to: "${messageContent}". In production, this would be the AI's analysis of your uploaded file "${activeChat.fileName}".`,
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      updateActiveChat({
        messages: [...activeChat.messages, userMessage, aiMessage],
      });
    } catch (error) {
      console.error("Message failed:", error);
      const errorMessage = {
        id: Date.now() + 1,
        content:
          "Sorry, I encountered an error processing your message. Please try again.",
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      updateActiveChat({
        messages: [...activeChat.messages, userMessage, errorMessage],
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-screen bg-gray-50 flex overflow-hidden">
      {/* Sidebar */}
      <Sidebar
        chats={chats}
        activeChat={activeChat}
        onSelectChat={selectChat}
        onNewChat={createNewChat}
        onDeleteChat={deleteChat}
        isMobileOpen={isMobileSidebarOpen}
        onCloseMobile={() => setIsMobileSidebarOpen(false)}
      />

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="px-6 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <button
                  onClick={() => setIsMobileSidebarOpen(true)}
                  className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
                >
                  <Menu className="w-6 h-6" />
                </button>
                <div className="bg-blue-600 p-2 rounded-lg">
                  <MessageSquare className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-gray-900">
                    {activeChat?.fileName || "AI Document Chat"}
                  </h1>
                  <p className="text-sm text-gray-600">
                    {activeChat
                      ? activeChat.uploadedFile
                        ? "Chat with your document"
                        : "Upload a document to start"
                      : "Select or create a conversation"}
                  </p>
                </div>
              </div>
              {activeChat?.uploadedFile && (
                <div className="flex items-center space-x-2 text-sm text-green-600">
                  <div className="w-2 h-2 bg-green-600 rounded-full animate-pulse"></div>
                  <span className="hidden sm:inline">Connected</span>
                </div>
              )}
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="flex-1 overflow-hidden">
          {!activeChat ? (
            <div className="h-full flex items-center justify-center p-8">
              <div className="text-center max-w-md">
                <div className="bg-blue-100 p-6 rounded-full mx-auto w-fit mb-4">
                  <MessageSquare className="w-16 h-16 text-blue-600" />
                </div>
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  Welcome to AI Document Chat
                </h2>
                <p className="text-gray-600 mb-6">
                  Create a new conversation to start chatting with your
                  documents
                </p>
                <button
                  onClick={createNewChat}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-colors inline-flex items-center space-x-2"
                >
                  <Plus className="w-5 h-5" />
                  <span>Create New Chat</span>
                </button>
              </div>
            </div>
          ) : (
            <div className="h-full flex flex-col">
              {!activeChat.uploadedFile ? (
                <div className="flex-1 flex items-center justify-center p-8">
                  <div className="max-w-md w-full">
                    <div className="bg-yellow-100 border border-yellow-300 rounded-lg p-4 mb-4 flex items-start space-x-3">
                      <AlertCircle className="w-5 h-5 text-yellow-600 shrink-0 mt-0.5" />
                      <div className="text-left">
                        <p className="text-sm font-semibold text-yellow-800">
                          Required
                        </p>
                        <p className="text-xs text-yellow-700">
                          Upload a document to start this conversation
                        </p>
                      </div>
                    </div>
                    <FileUploadCard
                      onFileSelect={handleFileSelect}
                      uploadedFile={activeChat.uploadedFile}
                      onRemoveFile={handleRemoveFile}
                    />
                  </div>
                </div>
              ) : (
                <>
                  <div className="border-b bg-gray-50 p-4">
                    <FileUploadCard
                      onFileSelect={handleFileSelect}
                      uploadedFile={activeChat.uploadedFile}
                      onRemoveFile={handleRemoveFile}
                    />
                  </div>

                  <div
                    ref={chatContainerRef}
                    className="flex-1 overflow-y-auto p-6 bg-white"
                  >
                    {activeChat.messages.length === 0 ? (
                      <EmptyState />
                    ) : (
                      activeChat.messages.map((msg) => (
                        <ChatMessage
                          key={msg.id}
                          message={msg}
                          isUser={msg.isUser}
                        />
                      ))
                    )}
                    {isLoading && (
                      <div className="flex justify-start mb-4">
                        <div className="bg-gray-100 rounded-2xl px-4 py-3">
                          <div className="flex space-x-2">
                            <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.1s" }}
                            ></div>
                            <div
                              className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                              style={{ animationDelay: "0.2s" }}
                            ></div>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>

                  <ChatInput
                    onSendMessage={handleSendMessage}
                    disabled={!activeChat.uploadedFile || isLoading}
                  />
                </>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
