from common_dependencies import TextLoader, RecursiveCharacterTextSplitter, LLMChainExtractor, OpenAIEmbeddings, Chroma, ChatOpenAI, ContextualCompressionRetriever

def initialize_chroma_db():
    loader = TextLoader('webscraped_data.txt', encoding='utf8')
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=100, separators=[" ", ",", "\n"])
    docs = text_splitter.split_documents(documents)

    embedding_function = OpenAIEmbeddings()
    chroma_db = Chroma.from_documents(docs, embedding_function, persist_directory='./medchroma_db')
    chroma_db.persist()

    return chroma_db

def initialize_rag_pipeline():
    llm = ChatOpenAI(temperature=0)
    compressor = LLMChainExtractor.from_llm(llm)
    db = initialize_chroma_db()
    compression_retriever = ContextualCompressionRetriever(base_compressor=compressor,
                                                           base_retriever=db.as_retriever())

    return compression_retriever

def get_compressed_docs(rag_pipeline, question):
    compressed_docs = rag_pipeline.get_relevant_documents(question)
    return compressed_docs[0].page_content
