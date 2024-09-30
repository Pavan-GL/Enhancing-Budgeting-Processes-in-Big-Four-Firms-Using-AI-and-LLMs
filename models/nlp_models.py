import os
import spacy
import logging
import pickle
from transformers import pipeline

# Set up logging
logging.basicConfig(filename='logs/document_processing.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class DocumentProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.summarizer = pipeline("summarization")

    def process_documents(self, documents):
        processed_texts = []
        try:
            for file in documents:
                text = file.read().decode('utf-8')  # Ensure you read the document correctly
                doc = self.nlp(text)
                processed_texts.append(doc.text)  # You could add more processing as needed
            logging.info("Successfully processed documents.")
        except Exception as e:
            logging.error(f"Error processing documents: {e}")
            raise
        return processed_texts

    def summarize_documents(self, documents):
        summaries = []
        try:
            for doc in documents:
                summary = self.summarizer(doc, max_length=150, min_length=40, do_sample=False)
                summaries.append(summary[0]['summary_text'])
            logging.info("Successfully generated summaries.")
        except Exception as e:
            logging.error(f"Error summarizing documents: {e}")
            raise
        return summaries

    def save_summarizer(self, filepath):
        try:
            with open(filepath, 'wb') as f:
                pickle.dump(self.summarizer, f)
            logging.info(f"Summarizer model saved to {filepath}.")
        except Exception as e:
            logging.error(f"Error saving summarizer model: {e}")
            raise

    def load_summarizer(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                self.summarizer = pickle.load(f)
            logging.info(f"Summarizer model loaded from {filepath}.")
        except Exception as e:
            logging.error(f"Error loading summarizer model: {e}")
            raise

# Example usage:
if __name__ == "__main__":
    processor = DocumentProcessor()
    # Load documents from a directory or any source
    documents = []  # Replace this with actual file objects, e.g., from Flask request.files
    processed_docs = processor.process_documents(documents)
    summaries = processor.summarize_documents(processed_docs)

    # Save the summarizer model if needed
    processor.save_summarizer('models/summarizer.pkl')

    # Load the summarizer model if needed
    # processor.load_summarizer('models/summarizer.pkl')
