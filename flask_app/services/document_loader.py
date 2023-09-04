from langchain.document_loaders.recursive_url_loader import RecursiveUrlLoader


class DocumentLoader:
    """
    Handles the loading of documents from a specified URL.

    __init__ Args:
        url (str): The URL from which to load documents.
    """

    def __init__(self, url: str) -> None:
        """Initializes the DocumentLoader with a URL."""
        self.url: str = url

    def load_documents(self) -> list:
        """
        Loads documents from the specified URL.

        Returns:
            list: A list of loaded documents.
        """
        print(f"\n{'_'*80}\n\nLoading documents from {self.url}...\n\n{'_'*80}")
        loader = RecursiveUrlLoader(url=self.url, prevent_outside=True, use_async=True)
        documents: list = loader.load()
        if len(documents) == 0:
            print(
                "\nWarning: No documents were loaded. Please check the URL or the RecursiveUrlLoader implementation.\n"
            )
        print(
            f"\n{'_'*80}\n\nLoaded {len(documents)} documents from {self.url}.\n\n{'_'*80}"
        )
        return documents
