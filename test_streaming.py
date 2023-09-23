from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.chains.llm import LLMChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains.conversational_retrieval.prompts import (
    CONDENSE_QUESTION_PROMPT,
    QA_PROMPT,
)
from langchain.chains.question_answering import load_qa_chain
from flask_app.services.vector_database import VectorDatabase

# Initialize the required objects (you can put this in an `__init__` method later)
vector_db = VectorDatabase()
llm = ChatOpenAI(temperature=0, model="gpt-4")
streaming_llm = ChatOpenAI(
    streaming=True, callbacks=[StreamingStdOutCallbackHandler()], temperature=0
)
question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
doc_chain = load_qa_chain(llm=streaming_llm, chain_type="stuff", prompt=QA_PROMPT)
qa_chain = ConversationalRetrievalChain(
    retriever=vector_db.database.as_retriever(
        search_type="mmr", search_kwargs={"k": 5, "fetch_k": 50}
    ),
    combine_docs_chain=doc_chain,
    question_generator=question_generator,
)


# The function to generate AI response without database calls
def generate_ai_response_no_db(user_query: str) -> str | None:
    if user_query.strip() == "":
        print("Message cannot be empty.")
        return

    print(f"\n{'_'*80}\nReceived user query: {user_query}\n{'_'*80}\n")

    # Generate AI response
    result: dict = qa_chain({"question": user_query, "chat_history": []})
    answer: str = result["answer"]
    print(f"\n{'_'*80}\nGenerated AI answer: {answer}\n{'_'*80}\n")

    return answer


# To run this function from the terminal, you can add something like this at the bottom of your file:
if __name__ == "__main__":
    user_input = input("Enter your query: ")
    generate_ai_response_no_db(user_input)
