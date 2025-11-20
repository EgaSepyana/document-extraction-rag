import { FileText, X } from "lucide-react";
import React from "react";

const SideBar = ({ chats, onChatAdd, onChatSelect, activeChat }) => {
  return (
    <div className="flex flex-col px-6 py-8 w-72 h-screen overflow-hidden border-r border-solid dark:border-primary-border-dark">
      <button
        onClick={onChatAdd}
        className="px-6 cursor-pointer mb-6 py-2 w-full bg-primary-base rounded-lg"
      >
        New Chat
      </button>

      {/* Chat List */}
      <h1 className="block text-xs opacity-70 mb-1">ACTIVE FILE</h1>
      <div className="flex hide-scrollbar overflow-y-auto flex-1">
        <div className="w-full flex flex-col gap-2.5">
          {chats &&
            chats.map((chat, i) => (
              <button
                onClick={() => onChatSelect(chat.id)}
                className={`${
                  activeChat?.id === chat.id ? "dark:bg-card-dark" : ""
                } cursor-pointer px-2 rounded-lg py-3 flex w-full items-center justify-between`}
              >
                <div className="flex items-center justify-start gap-2">
                  <FileText />
                  <p className="truncate max-w-[150px]">{chat.fileName}</p>
                </div>
                <X className="cursor-pointer w-5 h-5" />
              </button>
            ))}
        </div>
      </div>
      <div className="flex items-center justify-start gap-3 py-4 pb-8 border-t border-solid dark:border-primary-border-dark">
        <div className="w-10 h-10 bg-primary-base rounded-4xl overflow-hidden">
          <img
            src="https://i.pinimg.com/736x/bd/6f/99/bd6f99210ee96c2d334824352f12e2ff.jpg"
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
        <h1 className="text-md font-bold">Jhon Doe</h1>
      </div>
    </div>
  );
};

export default SideBar;
