from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

CAMINHO_DB = "db"

prompt_template = """
Responda a pergunta do usuário:
{pergunta} 

com base nessas informações abaixo:

{base_conhecimento}"""


def perguntar():
    pergunta = input("Escreva sua pergunta: ")

    # carregar o banco de dados
    funcao_embedding = OpenAIEmbeddings()
    db = Chroma(persist_directory=CAMINHO_DB,
                embedding_function=funcao_embedding)

    # comparar a pergunta do usuario (embedding) com o meu banco de dados
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=4)
    if len(resultados) == 0 or resultados[0][1] < 0.7:
        print("Não conseguiu encontrar alguma informação relevante na base")
        return

    textos_resultado = []
    for resultado in resultados:
        texto = resultado[0].page_content
        textos_resultado.append(texto)

    base_conhecimento = "\n\n----\n\n".join(textos_resultado)
    prompt = ChatPromptTemplate.from_template(prompt_template)
    prompt = prompt.invoke(
        {"pergunta": pergunta, "base_conhecimento": base_conhecimento})
    print(prompt)

    # Usando o modelo do ChatOpenAI para responder a pergunta do usuario
    modelo = ChatOpenAI()
    texto_resposta = modelo.invoke(prompt).content
    print("Resposta da IA:", texto_resposta)


perguntar()
