import { useEffect, useRef, useState } from "react";
import FileUploadCard from "./components/FileUploadCard";
import { Send } from "lucide-react";
import ChatMesseges from "./components/ChatMesseges";
import ChatInput from "./components/ChatInput";
import Loading from "./components/Loading";
import SideBar from "./components/SideBar";
import { NavBar } from "./components/NavBar";
import apiService from "./api/services/qna";
function App() {
  const sample_chat = {
    uploadedFile: null,
    fileName: null,
    messages: [
      {
        messege: "halo agent",
        isUser: true,
      },
      {
        messege: "halo ega",
        isUser: false,
      },
      {
        messege: "apakabar",
        isUser: true,
      },
      {
        messege: "baik , apakah ada yang bisa saya bantu?",
        isUser: false,
      },
      {
        messege: "ga ada",
        isUser: true,
      },
      {
        messege:
          "baik, jika ada yang ingin di tanyakan tanyakan saja jangan ragu",
        isUser: false,
      },
    ],
  };

  const [chats, setChats] = useState([]);
  const [activeChat, setActiveChat] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [chatLoading, setChatLoading] = useState(false);
  const [conversationLoading, setConversationLoading] = useState(false);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop =
        chatContainerRef.current.scrollHeight;
    }
  }, [activeChat?.messages]);

  const fetchChats = async () => {
    setChatLoading(true);

    const { data } = await apiService.getAllChats();

    let chats = data.map((chat) => ({
      id: chat.id,
      uploadedFile: null,
      fileName: chat.fileName,
      messages: [],
      createdAt: chat.createdAt,
    }));

    setChats(chats);
    setChatLoading(false);
  };

  const fetchConversaion = async (activeChat) => {
    setConversationLoading(true);

    const { data } = await apiService.getConversation(activeChat.id);

    // console.log(data);
    setActiveChat((prev) => ({
      ...prev,
      ...activeChat,
      ...{ messages: [...data] },
    }));
    setConversationLoading(false);
  };

  // get-all files
  useEffect(() => {
    fetchChats();
  }, []);

  const selectChat = (chatId) => {
    const chat = chats.find((c) => c.id === chatId);
    if (chat) {
      setActiveChat(chat);
      fetchConversaion(chat);
    }
  };

  const createNewChat = (newChat) => {
    setChats((prev) => [newChat, ...prev]);
  };

  const onNewChat = () => {
    setActiveChat(null);
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
    // console.log("FILE SELECTED");

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // API UPLOAD IMPLEMENTATION
      const reponse = await apiService.uploadFile(file);
      // console.log(reponse);

      const { file_name, id, created_at } = reponse.data;

      // API INDEX IMPLEMENTATION
      const indexing_response = await apiService.indexFile(id);

      const systemMesseges = {
        id: Date.now(),
        messege: `File "${file.name}" uploaded successfully! You can now start asking questions about the document.`,
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      const newChat = {
        id: id,
        uploadedFile: file,
        fileName: file_name,
        messages: [systemMesseges],
        createdAt: created_at,
      };

      createNewChat(newChat);
      setActiveChat((prev) => ({ ...prev, ...newChat }));
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Failed to upload file. Please try again.");
    }
  };

  const handleSendMessage = async (query) => {
    if (!activeChat) return;

    const userMessage = {
      id: Date.now(),
      messege: query,
      isUser: true,
      timestamp: new Date().toLocaleTimeString(),
    };

    updateActiveChat({
      messages: [...activeChat.messages, userMessage],
    });

    setIsLoading(true);

    try {
      await new Promise((resolve) => setTimeout(resolve, 1000));

      // API CHAT IMPLEMENTATION
      const chat_response = await apiService.sendChat(query, activeChat.id);
      const { answer } = chat_response.data;

      const aiMessage = {
        id: Date.now() + 1,
        messege: answer,
        isUser: false,
        timestamp: new Date().toLocaleTimeString(),
      };

      updateActiveChat({
        messages: [...activeChat.messages, userMessage, aiMessage],
      });
    } catch (error) {
      console.log("Messege Failed : ", error);

      const errorMessage = {
        id: Date.now() + 1,
        messege:
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

    // console.log(query);
  };

  return (
    <main className="dark:text-white pt-12.5 h-screen flex overflow-hidden">
      <SideBar
        chats={chats}
        onChatAdd={onNewChat}
        onChatSelect={selectChat}
        activeChat={activeChat}
      />
      <div className="flex-1 flex flex-col overflow-hidden">
        <NavBar />

        <section
          className={`container px-20 h-full w-full mx-auto ${
            !activeChat ? "mt-14" : "mt-4"
          } flex flex-col overflow-hidden`}
        >
          {/* If The File Is Not Exist*/}
          <div className="h-full flex-1 flex flex-col w-full overflow-hidden">
            <div
              ref={chatContainerRef}
              className="font-semibold flex-1 overflow-y-auto hide-scrollbar"
            >
              {!activeChat ? (
                <div>
                  <h1 className="text-5xl mb-4">
                    Start By Uploading Your Document
                  </h1>
                  <h1 className="text-xl text-font-secondary mb-10">
                    Supported formats: PDF,DOCS,CSV
                  </h1>
                  <FileUploadCard
                    onFileSelect={handleFileSelect}
                    onRemoveFile={() => {}}
                    uploadedFile={activeChat?.uploadedFile}
                  />
                </div>
              ) : (
                <>
                  {activeChat.messages.map((item) => (
                    <ChatMesseges key={item.id} item={item} />
                  ))}
                  {isLoading && <Loading />}
                </>
              )}
            </div>
            <ChatInput
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              disabled={!activeChat}
            />
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;
