import os

from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.document_loaders import UnstructuredHTMLLoader
import streamlit as st



os.environ['OPENAI_API_KEY'] = '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'
default_doc_name = 'Documento-de-examen-Grupo1.html'



# Load the document, split it into chunks, embed each chunk and load it into the vector store.
#raw_documents = TextLoader('../../../Documento-de-examen-Grupo1.txt').load()
#text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#documents = text_splitter.split_documents(raw_documents)
#db = FAISS.from_documents(documents, OpenAIEmbeddings())


def process_doc(
        path: str = 'https://mega.nz/file/ZhFAAADQ#pcH4drbs_teFgfGyIdS5gdyl7fkE6B22owRlxqYoyRM',
        is_local: bool = False,
        question: str = 'Cuál es la idea principal?'
):
    _, loader = os.system(f'curl -o {default_doc_name} {path}'), TextLoader(f"./{default_doc_name}") if not is_local \
        else TextLoader(path)

    doc = loader.load_and_split()
    print(doc[-1])
    db = FAISS.from_documents(doc, embedding=OpenAIEmbeddings())
    qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=db.as_retriever())
    st.write(qa.run(question))

def client():
    st.title('EJERCICIO DE PRUEBA')
    uploader = st.file_uploader('Subir ', type='html')
    #loader = BSHTMLLoader("Documento-de-examen-Grupo1.html")

    if uploader:
        with open(f'./{default_doc_name}', 'wb') as f:
            f.write(uploader.getbuffer())
        st.success('El html ha sido guardado de forma correcta')

    question = st.text_input('Realiza una pregunta? ',
                             placeholder='Pregunta para el html', disabled=not uploader)

    if st.button('Enviar Pregunta'):
        if uploader:
            process_doc(
                path=default_doc_name,
                is_local=True,
                question=question
            )
        else:
            st.info('Cargando ')
            process_doc()


if __name__ == '__main__':
    client()
    #process_doc()