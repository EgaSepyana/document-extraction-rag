import { Send } from "lucide-react";
import React, { useState } from "react";

const ChatInput = ({ onSendMessage, disabled, isLoading }) => {
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
    <div className="mb-6 rounded-lg dark:bg-button-bg-primary overflow-hidden">
      <div className="flex space-x-3">
        <input
          className="flex-1 border-gray-300 rounded-lg px-4 py-3 focus:outline-none disabled:cursor-not-allowed"
          type="text"
          value={input}
          disabled={isLoading ? !disabled : disabled}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={
            disabled
              ? "Chat Is locked until a file uploaded......"
              : "Ask a question about your document.."
          }
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !input.trim()}
          className="bg-primary-base hover:bg-primary-base/80 disabled:bg-primary-base/50 disabledR:cursor-not-allowed text-white px-6 py-3 rounded-lg transition-colors flex items-center space-x-2"
        >
          <Send className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
};

export default ChatInput;
