from langchain.document_transformers import BeautifulSoupTransformer


class DocumentTransformer:
    """
    Handles the transformation of documents.

    Notes:
        Currently, it uses BeautifulSoup for HTML parsing and transformation.
    """

    def soup_transform(self, documents: list) -> list:
        """
        Transforms the list of documents using the BeautifulSoupTransformer model from langchain.

        Args:
            documents (list): The list of documents to transform.

        Returns:
            list: The list of transformed documents.
        """
        print(f"\n{'_'*80}\n\nTransforming documents...\n\n{'_'*80}")
        bs_transformer = BeautifulSoupTransformer()
        transformed_documents: list = bs_transformer.transform_documents(documents=documents)  # type: ignore
        print(
            f"\n{'_'*80}\n\nTransformed {len(transformed_documents)} documents.\n\n{'_'*80}"
        )
        return transformed_documents
