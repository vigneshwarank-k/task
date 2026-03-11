from langchain_openai import ChatOpenAI, OpenAIEmbeddings

chat_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

embeddings = OpenAIEmbeddings()
