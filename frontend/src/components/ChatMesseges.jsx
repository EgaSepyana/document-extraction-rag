import React from "react";
import logo from "../../src/assets/Logo.svg";

const ChatMesseges = ({item}) => {
  return (
    <div
      className={`flex ${
        item.isUser ? "justify-end" : "justify-end flex-row-reverse"
      } items-end mb-4 gap-3`}
    >
      <div className="max-w-[50%] flex flex-col gap-2">
        <div
          className={`flex ${
            item.isUser ? "justify-end" : "justify-start"
          } items-center gap-2`}
        >
          {/* <span className="text-sm opacity-70">You</span> */}
          <span className="text-xs opacity-70">
            {item.isUser ? "You" : "Raga Agent"}
          </span>
        </div>
        <div
          className={`rounded-2xl px-4 py-3 ${
            item.isUser ? "bg-primary-base" : "dark:bg-card-dark"
          } text-white`}
        >
          <p className="text-sm whitespace-pre-wrap">{item.messege}</p>
        </div>
      </div>
      <div className="">
        <div className="w-12 h-12 rounded-4xl overflow-hidden">
          <img
            src={
              item.isUser
                ? "https://i.pinimg.com/736x/bd/6f/99/bd6f99210ee96c2d334824352f12e2ff.jpg"
                : logo
            }
            alt=""
            className="w-full h-full object-cover"
          />
        </div>
      </div>
    </div>
  );
};

export default ChatMesseges;
