from ragas.llms.prompt import Prompt
from langchain_openai.chat_models import ChatOpenAI
from ragas.llms.base import LangchainLLMWrapper
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Obter a chave de API da variável de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

# Verificar se a chave de API foi carregada corretamente
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY não está definida. Verifique se o arquivo .env está configurado corretamente.")
else:
  print("api passou")



openai_model = ChatOpenAI(model="gpt-3.5-turbo")

openai_model = LangchainLLMWrapper(openai_model)
noun_extractor = Prompt(
    name="noun_extractor",
    instruction="Extract the noun from given sentence",
    examples=[{
        "sentence":"The sun sets over the mountains.",
        "output":{"nouns":["sun", "mountains"]}
    }],
    input_keys=["sentence"],
    output_key="output",
    output_type="json"
)