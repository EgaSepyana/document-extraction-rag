const API_CONFIG = {
  baseURL: "http://localhost:44109",
  endpoints: {
    upload: "/qna/upload",
    index: "/qna/index",
    chat: "/qna/chat",
    getAllDocs: "/qna/docs/get-all",
    getOneDocs: "/qna/docs/{id}",
    getConversation: "/qna/docs/conversation",
  },
};

export default API_CONFIG;
