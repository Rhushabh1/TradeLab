from openai import OpenAI 

from ai_worker.prompt_builder import build_prompt


client = OpenAI()


# TODO - update the airequest table with the status and do error handling
def generate(question, context):
	prompt = build_prompt(question, context)
	response = client.chat.completions.create(model = "gpt-4o-mini",
												messages = [{
															"role": "user",
															"content": prompt
															}])
	return response.choices[0].message.content