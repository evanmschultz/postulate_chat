from threading import Thread
from flask_app.models.vector_database import VectorDatabase
from flask_app.models.document_loader import DocumentLoader
from flask_app.models.document_transformer import DocumentTransformer
from flask_app.models.text_splitter import TextSplitter
from flask_app.models.utility_functions import UtilityFunctions
import os


class IngestionManager:
    """
    Manages the ingestion process for a list of URLs, including document loading, transformation, and text splitting.

    __init__ Args:
        urls (list): The list of URLs to ingest.
        vector_db (VectorDatabase): The vector database to store the processed documents.
    """

    def __init__(self, urls: list, vector_db: "VectorDatabase") -> None:
        """Initializes the IngestionManager"""
        self.urls: list = urls
        self.vector_db: VectorDatabase = vector_db

    def ingest_urls(self):
        """
        Starts the ingestion process for the list of URLs. This method leverages Python's threading
        library to ingest multiple URLs in parallel to speed up the overall ingestion process.

        Returns:
            None

        How it works:
            - Creates an empty list `threads` to hold Thread objects.
            - Iterates through the list of URLs, creating a new Thread for each URL.
            - Starts each Thread to process the URL using the `ingest_single_url` method.
            - Waits for all Threads to complete their execution with `join()`.
        """
        print("Starting ingestion process...")
        threads: list = []
        for url in self.urls:
            thread = Thread(target=self.ingest_single_url, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        print("Ingestion process completed.")

    def ingest_single_url(self, url: str) -> None:
        """
        Ingests and processes information from a single URL and saves it to the vector database.

        Args:
            url (str): The URL to ingest.

        Returns:
            None

        What it does:
            1. Create a directory if it doesn't exist to save the scraped documents.
            2. Load the documents from the URL using the DocumentLoader class.
            3. Transform the documents into a more manageable form using the DocumentTransformer class.
            4. Save the transformed documents to disk.
            5. Split the text in the documents into smaller chunks using the TextSplitter class.
            6. Add the split documents to the vector database for later querying.
        """
        print(f"\n{'_'*80}\n\nProcessing URL: {url}...\n\n{'_'*80}")
        folder_path: str = "docs/scraped_sites"
        UtilityFunctions.create_directory(folder_path)

        # Load
        doc_loader = DocumentLoader(url)
        documents: list = doc_loader.load_documents()

        # Transform
        doc_transformer = DocumentTransformer()
        transformed_documents: list = doc_transformer.soup_transform(documents)  # type: ignore

        # Save Transformed Documents
        for doc in transformed_documents:
            sanitized_title: str = UtilityFunctions.sanitize_filename(
                doc.metadata["title"]
            )
            filename: str = f"{sanitized_title}.txt"
            UtilityFunctions.save_to_txt_file(
                os.path.join(folder_path, filename), doc.page_content
            )
            print(f"\n{'_'*80}\n\nSaved transformed document: {filename}\n\n{'_'*80}")

        # Split Text
        text_splitter = TextSplitter()
        split_documents: list = text_splitter.split_text(transformed_documents)

        # Save to Vector Database
        self.vector_db.add_documents(split_documents)
        print(f"\n{'_'*80}\n\nProcessing for {url} completed.\n\n{'_'*80}")
