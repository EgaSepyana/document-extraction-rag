import pymupdf
from loguru import logger
from langchain_text_splitters import RecursiveCharacterTextSplitter , NLTKTextSplitter
import nltk
nltk.download("punkt")
import re

class Extraktor:
    def __init__(self):
        pass

    def extract_file(self , file_path):

        file_ext = file_path.split(".")[-1]

        texts = []

        match file_ext:
            case "pdf":
                texts = self.extract_text_from_pdf(file_path) 

        # chunk = self.indexing_text(texts)
        return texts

    def extract_text_from_pdf(self , file_path:str):
        doc = pymupdf.open(file_path)  # open a document
        
        logger.info(f"Total Pages : {doc.page_count}")
        # chunk_size = 500
        # chunk_overlap = 50
        
        # if doc.page_count >= 15:
        #     chunk_size = 1000
        #     chunk_overlap = 150

        texts = []
        for page_num, page in enumerate(doc):
            page = doc.load_page(page_num)
            text = page.get_text("text")

            if not text.strip():
                continue

            texts.append({
                "text" : text,
                "page" : page_num
            })

        return texts

    def clean_text(self, text:str):
        text = text.replace("-\n", "")
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r'\.\s+"', '." ', text)
        return text.strip()

    def chunk_text(self , text, chunk_size=300, overlap=50):
        text = self.clean_text(text)

        splitter = NLTKTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap
        )

        return splitter.split_text(text)

    def indexing_text(self, extract_text , chunk_size: int = 300 , chunk_overlap: int = 50):

        # chunk_size = 500
        # chunk_overlap = 50
        
        # if len(extract_text) >= 15:
        # chunk_size = 1000
        # chunk_overlap = 150
        
        texts = extract_text

        if isinstance(extract_text , list):
            texts = "".join([text["text"] for text in extract_text])
        # print(texts)

        chunks = self.chunk_text(text=texts , chunk_size=chunk_size , overlap=chunk_overlap)
        # logger.info(chunks)
        return chunks

    def extract_text_from_docs(self):
        pass

    def extract_text_from_csv(self):
        pass


if __name__ == "__main__":
    extractor = Extraktor()
    extractor.extract_file()
