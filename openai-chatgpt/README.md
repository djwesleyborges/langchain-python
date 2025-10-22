# Langchain Python

Projeto simples que demonstra como construir uma base de conhecimento vetorial usando PDFs, persisti-la com Chroma e fazer consultas em linguagem natural usando modelos de chat.

Este repositório contém scripts mínimos para:

- Extrair textos de PDFs na pasta `base/` e criar chunks (fragmentos) de texto.
- Gerar embeddings com OpenAI (ou outro provedor conectado) e persistir um banco de dados Chroma em `db/`.
- Fazer perguntas ao banco de conhecimento usando similaridade por embeddings e um modelo de chat (ChatOpenAI).

## Estrutura do projeto

- `criar_db.py` - Carrega PDFs da pasta `base/`, divide em chunks e cria um banco Chroma persistente em `db/`.
- `main.py` - Script interativo que solicita uma pergunta ao usuário, busca documentos semelhantes no Chroma e gera uma resposta com um modelo de chat.
- `requirements.txt` - Dependências do projeto.
- `base/` - Local onde os PDFs a serem indexados devem ser colocados.
- `db/` - Diretório onde o Chroma persiste os dados (já pode conter um banco gerado).

## Requisitos

- Python 3.8+
- Chaves/serviços necessários conforme o provedor de embeddings e do modelo de chat que você usar (ex.: OpenAI). Veja `requirements.txt` para bibliotecas.

Dependências principais (conforme `requirements.txt`):

- python-dotenv
- langchain
- langchain-chroma
- langchain-community
- langchain-openai
- chromadb
- pypdf

Instale com:

```bash
pip install -r requirements.txt
```

## Configuração

1. Crie um arquivo `.env` (opcional) na raiz do projeto para armazenar variáveis de ambiente utilizadas pelo provedor de embeddings / chat. Exemplo mínimo:

```
OPENAI_API_KEY=sk-...
```

Observação: os scripts usam as classes de embeddings e modelos expostas pelo pacote `langchain_openai` no projeto — adapte para o provedor que você utiliza conforme necessário.

## Como gerar a base de conhecimento (indexar PDFs)

1. Coloque seus arquivos PDF em `base/`.
2. Execute:

```bash
python criar_db.py
```

O script `criar_db.py` irá:

- Carregar todos os PDFs em `base/`.
- Dividir o conteúdo em chunks (tamanho 2000, overlap 500).
- Gerar embeddings com `OpenAIEmbeddings` e persistir no diretório `db/`.

Ao final você verá a mensagem "Banco de Dados criado" quando concluído.

## Como consultar a base (fazer perguntas)

Execute o script interativo:

```bash
python main.py
```

Ele pedirá que você digite uma pergunta. O fluxo é:

1. Gerar embedding da pergunta.
2. Buscar os 4 documentos mais relevantes em `db/`.
3. Se a similaridade do melhor resultado for menor que 0.7, o script avisa que não encontrou informação relevante.
4. Caso contrário, constrói um prompt combinando a pergunta e os trechos mais relevantes e chama o modelo de chat para gerar uma resposta.

## Contrato rápido (inputs/outputs)

- Inputs: PDFs em `base/` para indexação; texto de pergunta via stdin para `main.py`.
- Outputs: Banco persistente em `db/` e respostas impressas no terminal.
- Erros comuns: falta de chave da API ou modelo local não disponível; arquivos PDF inválidos.

## Dicas e edge cases

- Caso use OpenAI, defina `OPENAI_API_KEY` no `.env` ou no ambiente.
- Se o diretório `db/` já existir com dados, `criar_db.py` vai sobrescrever/atualizar conforme o comportamento do Chroma usado.
- Tenha atenção ao custo de geração de embeddings/consultas se usar um provedor pago.
