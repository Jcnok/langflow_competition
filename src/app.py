from dotenv import load_dotenv
import os
from langflow.load import run_flow_from_json
# Obter a chave de API da variável de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")
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