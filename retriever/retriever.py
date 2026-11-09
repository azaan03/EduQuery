
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# Initialize embedding model
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Build retriever from PDF
def build_retriever_from_pdf(pdf_path: str):

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )


# Create separate retrievers
academic_retriever = build_retriever_from_pdf(
    "data/academics_handbook.pdf"
)

fee_retriever = build_retriever_from_pdf(
    "data/fee_structure.pdf"
)
