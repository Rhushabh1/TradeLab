def build_prompt(question, context):
	joined = "\n\n".join(context)
	return f"""
			You are a stock research assistant.
			Use ONLY the information below.
			Context: 
			{joined}
			Question: 
			{question}
			Answer: 
			"""