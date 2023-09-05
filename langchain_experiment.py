from dotenv import load_dotenv
load_dotenv()
import os

# Update the path to include the absolute path and the .env file
env_path = '/Users/tdentry/keys/openai/.env'
load_dotenv(dotenv_path=env_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
# from langchain.document_loaders import TextLoader
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.text_splitter import CharacterTextSplitter
from pprint import pprint
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
import json
from pathlib import Path
from pprint import pprint
# from langchain.document_loaders import JSONLoader

# def ai_studio_demo(question):
#     '''
#     1. Takes in a question about the information from the target website and returns the most relevant
#     answer
#     2. Load the dataset obtained via scraping a customer website
#     '''
#     # step 1:  Load webscaped_data dict from the project path

# step 2: Load the scraped data into ChromaDB and convert data_dict into Document objects
# note that I am NOT splitting or chunking as the corpora is relatively small
# if so, this would be done with the CharacterTextSplitter.from_tiktoken_encoder(chunk_size=n or something else)

file_path='/Users/tdentry/repos/vonage/PatientNow App/webscraped_data.json'
data = json.loads(Path(file_path).read_text())
for k, v in data.items():
    pprint(v)  # Directly print the procedure content
    print('-' * 40)  # Separate content from different procedures

# loader = JSONLoader(
#     file_path='webscraped_data.json',
#     jq_schema='.messages[].content')

data = loader.load()
# loader = JSONLoader(
#     file_path='./Users/tdentry/repos/vonage/PatientNow App/webscraped_data.json',
#     jq_schema='.messages[].content')


# documents = [Document(key=procedure_name, value=procedure_content) for procedure_name, procedure_content in data_dict.items()]
# retriever = EmbeddingRetriever(documents=documents)
# db = Chroma(retriever=retriever, persist_directory='./db_persist')
# db.persist
# # step 3: Initialize the language model
# llm = ChatOpenAI(temperature=0)
# compressor = LLMChainExtractor.from_llm(llm)
#
# # step 4: Initialize the ContextualCompressionRetriever
# compression_retreiver = ContextualCompressionRetriever(base_compressor=compressor, base_retriever=db.as_retriever())
# compressed_docs = compression_retreiver.get_relevant_documents(question)
#
# # step 4: Use the question to look up relevant content from the data_dict
# if question in data_dict:
#     answer = data_dict[question]
#     return answer
# elif compressed_docs:
#     return compressed_docs[0].page_content
# else:
#     return "I'm sorry, I don't have information about that procedure."
