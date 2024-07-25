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
from datasets import Dataset 
from ragas.metrics import faithfulness, answer_correctness
from ragas import evaluate

data_samples = {
    'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
    'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
    'ground_truth': ['The first superbowl was held on January 15, 1967', 'The New England Patriots have won the Super Bowl a record six times']
}
dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset,metrics=[answer_correctness])
score.to_pandas()



from datasets import Dataset 
from ragas.metrics.critique import harmfulness
from ragas import evaluate

data_samples = {
    'question': ['When was the first super bowl?', 'Who won the most super bowls?'],
    'answer': ['The first superbowl was held on Jan 15, 1967', 'The most super bowls have been won by The New England Patriots'],
    'contexts' : [['The First AFL–NFL World Championship Game was an American football game played on January 15, 1967, at the Los Angeles Memorial Coliseum in Los Angeles,'], 
    ['The Green Bay Packers...Green Bay, Wisconsin.','The Packers compete...Football Conference']],
}
dataset = Dataset.from_dict(data_samples)
score = evaluate(dataset,metrics=[harmfulness])
score.to_pandas()


from ragas.llms.prompt import Prompt

qa_prompt = Prompt(
    name="question_generation",
    instruction="Generate a question for the given answer",
    examples=[
        {
            "answer": "The last Olympics was held in Tokyo, Japan.",
            "context": "The last Olympics was held in Tokyo, Japan. It is held every 4 years",
            "output": {"question":"Where was the last Olympics held?"},
        },
        {
            "answer": "It can change its skin color based on the temperature of its environment.",
            "context": "A recent scientific study has discovered a new species of frog in the Amazon rainforest that has the unique ability to change its skin color based on the temperature of its environment.",
            "output": {"question":"What unique ability does the newly discovered species of frog have?"},
        }
    ],
    input_keys=["answer", "context"],
    output_key="output",
    output_type="json",
)