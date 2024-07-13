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
from langflow.load import run_flow_from_json

TWEAKS = {
  "ParseData-v44gO": {},
  "Prompt-8gSmO": {},
  "OpenAIModel-o5tIk": {"openai_api_key":openai_api_key},
  "ChatOutput-jb3cX": {},
  "File-auXkC": {},
  "ChatOutput-siTeg": {},
  "GroupNode-k67Uv": {}
}

result = run_flow_from_json(flow="submission_3.json", 
                            input_value="message",
                            fallback_to_env_vars=True, # False by default
                            tweaks=TWEAKS)
print(result)