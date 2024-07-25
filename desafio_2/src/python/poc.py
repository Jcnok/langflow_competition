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

BASE_API_URL = "http://127.0.0.1:7860/api/v1/run"
FLOW_ID = "2c735208-f996-4c38-b008-4993e0e3d697"
ENDPOINT = "" # You can set a specific endpoint name in the flow settings

# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "ChatInput-CRyYb": {
    "files": "",
    "input_value": "quantos cortes são necessários para dividir uma torta de maçã até chegar a um átomo? \n",
    "sender": "User",
    "sender_name": "User",
    "session_id": "",
    "store_message": True
  },
  "ParseData-dVnIO": {
    "sep": "\n",
    "template": "{text}"
  },
  "Prompt-CqGSl": {
    "context": "",
    "template": "{context}\n\n---\n\nVocê é um especialista em Cosmos, o livro Cosmos de Carl Sagan está no context. Responda as perguntas com base no conhecimento contido neste livro que está no context. Seja conciso, objetivo e forneça apenas a resposta direta, sem explicações adicionais. Por exemplo:\nGiven the context above, answer the question as best as possible.\nResponda apenas o que estiver no contexto, não adiciona nada de conteúdo externo.\nPergunta: {perguntas}\n\nResposta: ",
    "perguntas": ""
  },
  "OpenAIEmbeddings-OZVhU": {
    "chunk_size": 1000,
    "client": "",
    "default_headers": {},
    "default_query": {},
    "deployment": "",
    "dimensions": None,
    "embedding_ctx_length": 1536,
    "max_retries": 3,
    "model": "text-embedding-3-small",
    "model_kwargs": {},
    "openai_api_base": "",
    "openai_api_key": "sua chave api aqui",
    "openai_api_type": "",
    "openai_api_version": "",
    "openai_organization": "",
    "openai_proxy": "",
    "request_timeout": None,
    "show_progress_bar": False,
    "skip_empty": False,
    "tiktoken_enable": True,
    "tiktoken_model_name": ""
  },
  "Chroma-KHNHV": {
    "allow_duplicates": False,
    "chroma_server_cors_allow_origins": "",
    "chroma_server_grpc_port": None,
    "chroma_server_host": "",
    "chroma_server_http_port": None,
    "chroma_server_ssl_enabled": False,
    "collection_name": "langflow-cosmos",
    "limit": None,
    "number_of_results": 5,
    "persist_directory": "",
    "search_query": "",
    "search_type": "Similarity"
  },
  "LangWatchEvaluatorComponent-3EbHf": {
    "answer": "",
    "ground_truth": "",
    "question": "",
    "question_id": "",
    "user_cpf": "",
    "user_email": "",
    "user_name": ""
  },
  "TextOutput-cSeay": {
    "input_value": ""
  },
  "TextInput-tZhUm": {
    "input_value": "Cerca de noventa cortes. \n"
  },
  "ChatOutput-ZMPnN": {
    "data_template": "{text}",
    "input_value": "",
    "sender": "Machine",
    "sender_name": "AI",
    "session_id": "",
    "should_store_message": True
  },
  "OpenAIModel-2bfh7": {
    "input_value": "",
    "json_mode": False,
    "max_tokens": None,
    "model_kwargs": {},
    "model_name": "gpt-3.5-turbo",
    "openai_api_base": "",
    "openai_api_key": "sua chave api aqui",
    "output_schema": {},
    "seed": 1,
    "stream": False,
    "system_message": "",
    "temperature": 0.1
  },
  "StoreMessage-F6NTE": {
    "message": "",
    "sender": "AI",
    "sender_name": "AI",
    "session_id": "teste1"
  },
  "SaveToCSV-DXXUP": {
    "filename": "results/link.csv"
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
