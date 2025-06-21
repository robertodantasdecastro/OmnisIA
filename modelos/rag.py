"""Pipeline simples de RAG utilizando LangChain."""
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFacePipeline


def build_rag(model_id: str, retriever) -> RetrievalQA:
    llm = HuggingFacePipeline.from_model_id(model_id=model_id)
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    return chain
