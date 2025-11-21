import axios from "axios";
import API_CONFIG from "../config";

const apiService = {
  uploadFile: async (file) => {
    const formData = new FormData();
    formData.append("file", file);
    // formData.append("category", "Document");
    // formData.append("description", "This Document");

    try {
      const response = await axios.post(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.upload}`,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          params: {
            category: "Document",
            description: "This Document",
          },
        }
      );

      return response.data;
    } catch (err) {
      throw new Error("Upload failed");
    }
  },

  indexFile: async (document_id) => {
    try {
      const response = await axios.post(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.index}`,
        {
          document_id: document_id,
          chunk_size: 300,
          overlap_size: 50,
        }
      );

      return response.data;
    } catch (err) {
      throw new Error("Message failed");
    }
  },

  sendChat: async (question, document_id) => {
    try {
      const response = await axios.post(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.chat}`,
        { question, document_id }
      );

      return response.data;
    } catch (err) {
      throw new Error("Message failed");
    }
  },

  getAllChats: async () => {
    try {
      const default_parameter = {
        orderBy: "createdAt",
        order: "desc",
        page: 1,
        size: 10,
      };

      const response = await axios.post(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.getAllDocs}`,
        default_parameter
      );

      return response.data;
    } catch (err) {
      throw new Error("Message failed");
    }
  },

  getConversation: async (document_id) => {
    try {
      const response = await axios.get(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.getConversation}/${document_id}`
      );

      return response.data;
    } catch (err) {
      throw new Error("Message failed");
    }
  },

  getOneDocs: async (document_id) => {
    try {
      const response = await axios.get(
        `${API_CONFIG.baseURL}${API_CONFIG.endpoints.getOneDocs}/${document_id}`
      );

      return response.data;
    } catch (err) {
      throw new Error("Message failed");
    }
  },
};

export default apiService;
