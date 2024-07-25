import argparse
import json
from argparse import RawTextHelpFormatter
import requests
from typing import Optional
import warnings
try:
    from langflow.load import upload_file
except ImportError:
    warnings.warn("Langflow provides a function to help you upload files to the flow. Please install langflow to use it.")
    upload_file = None
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
BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "0c21b5fd-e18d-42fe-84a6-adfe82a1647d"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ParseData-HL2NO": {
    "sep": "\n",
    "template": "{text}"
  },
  "Prompt-ohi8K": {
    "template": "{conteúdo}\n\ncrie um resumo com as principais palavras compostas do conteúdo, seja específico e não ultrapasse 300 caracteres.\nResumo: ",
    "conteúdo": ""
  },
  "OpenAIModel-Y3MWq": {
    "input_value": "",
    "json_mode": False,
    "max_tokens": 1000,
    "model_kwargs": {},
    "model_name": "gpt-3.5-turbo",
    "openai_api_base": "",
    "openai_api_key": openai_api_key,
    "output_schema": {},
    "seed": 1,
    "stream": False,
    "system_message": "",
    "temperature": 0.3
  },
  "File-OGgXd": {
    "path": "desafio1.md",
    "silent_errors": False
  },
  "ChatOutput-uEBVN": {
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "Score",
    "session_id": "",
    "store_message": True
  },
  "GroupNode-ySC47": {
    "chunk_size": 1000,
    "client": "",
    "code": "from langflow.custom import Component\nfrom langflow.helpers.data import data_to_text\nfrom langflow.io import DataInput, MultilineInput, Output, StrInput\nfrom langflow.schema.message import Message\n\n\nclass ParseDataComponent(Component):\n    display_name = \"Parse Data\"\n    description = \"Convert Data into plain text following a specified template.\"\n    icon = \"braces\"\n\n    inputs = [\n        DataInput(name=\"data\", display_name=\"Data\", info=\"The data to convert to text.\"),\n        MultilineInput(\n            name=\"template\",\n            display_name=\"Template\",\n            info=\"The template to use for formatting the data. It can contain the keys {text}, {data} or any other key in the Data.\",\n            value=\"{text}\",\n        ),\n        StrInput(name=\"sep\", display_name=\"Separator\", advanced=True, value=\"\\n\"),\n    ]\n\n    outputs = [\n        Output(display_name=\"Text\", name=\"text\", method=\"parse_data\"),\n    ]\n\n    def parse_data(self) -> Message:\n        data = self.data if isinstance(self.data, list) else [self.data]\n        template = self.template\n\n        result_string = data_to_text(template, data, sep=self.sep)\n        self.status = result_string\n        return Message(text=result_string)\n",
    "default_headers": {},
    "default_query": {},
    "deployment": "",
    "embedding_ctx_length": 1536,
    "max_retries": 3,
    "model": "text-embedding-3-small",
    "model_kwargs": {},
    "openai_api_base": "",
    "openai_api_key": openai_api_key,
    "openai_api_type": "",
    "openai_api_version": "",
    "openai_organization": "",
    "openai_proxy": "",
    "request_timeout": 3,
    "show_progress_bar": False,
    "skip_empty": False,
    "tiktoken_enable": True,
    "tiktoken_model_name": "",
    "input_message": "",
    "sep": "\n",
    "template": "Score Inicial: {similaridade}\nFator de Redução: {fator_reducao} (1.0 = sem redução)\nScore Final: {score_final}\n"
  },
  "TextOutput-fqVwp": {
    "input_value": ""
  }
}

def run_flow(message: str,
  endpoint: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  api_key: Optional[str] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param endpoint: The ID or the endpoint name of the flow
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{BASE_API_URL}/{endpoint}"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if api_key:
        headers = {"x-api-key": api_key}
    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()

def main():
    parser = argparse.ArgumentParser(description="""Run a flow with a given message and optional tweaks.
Run it like: python <your file>.py "your message here" --endpoint "your_endpoint" --tweaks '{"key": "value"}'""",
        formatter_class=RawTextHelpFormatter)
    parser.add_argument("message", type=str, help="The message to send to the flow")
    parser.add_argument("--endpoint", type=str, default=ENDPOINT or FLOW_ID, help="The ID or the endpoint name of the flow")
    parser.add_argument("--tweaks", type=str, help="JSON string representing the tweaks to customize the flow", default=json.dumps(TWEAKS))
    parser.add_argument("--api_key", type=str, help="API key for authentication", default=None)
    parser.add_argument("--output_type", type=str, default="chat", help="The output type")
    parser.add_argument("--input_type", type=str, default="chat", help="The input type")
    parser.add_argument("--upload_file", type=str, help="Path to the file to upload", default=None)
    parser.add_argument("--components", type=str, help="Components to upload the file to", default=None)

    args = parser.parse_args()
    try:
      tweaks = json.loads(args.tweaks)
    except json.JSONDecodeError:
      raise ValueError("Invalid tweaks JSON string")

    if args.upload_file:
        if not upload_file:
            raise ImportError("Langflow is not installed. Please install it to use the upload_file function.")
        elif not args.components:
            raise ValueError("You need to provide the components to upload the file to.")
        tweaks = upload_file(file_path=args.upload_file, host=BASE_API_URL, flow_id=ENDPOINT, components=args.components, tweaks=tweaks)

    response = run_flow(
        message=args.message,
        endpoint=args.endpoint,
        output_type=args.output_type,
        input_type=args.input_type,
        tweaks=tweaks,
        api_key=args.api_key
    )

    print(json.dumps(response, indent=2))

if __name__ == "__main__":
    main()
