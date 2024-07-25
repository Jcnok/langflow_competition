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
  print(openai_api_key)   