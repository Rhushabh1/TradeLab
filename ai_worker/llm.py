from openai import OpenAI 

from app.config import settings
from ai_worker.prompt_builder import build_prompt


# ai response generator (main workhorse for ai worker)
# TODO - add error handling
def generate(question: str, context: list[str]) -> str:
	if not settings.OPENAI_API_KEY:
		raise RuntimeError("OPENAI_API_KEY is not configured")
	client = OpenAI(api_key = settings.OPENAI_API_KEY, timeout = 60, max_retries = 2)
	response = client.chat.completions.create(model = settings.OPENAI_MODEL,
											messages = [{
														"role": "system",
														"content": "You are a stock research assistant. Ground your answers in provided evidence"
														},
														{
														"role": "user",
														"content": build_prompt(question, answer)
														}],
											# tuning randomness
											temperature = 0.2
											)
	answer = response.choices[0].message.content
	if not answer:
		raise RuntimeError("AI provided empty response")
	return answer