def build_prompt(question: str, context: list[str]) -> str:
	joined = "\n\n".join(context) if context else "No relevant docs were found in user's watchlist data"
	return f"""You are TradeLab, a stock research assistant.
			Use the supplied context as your evidence. Do not invent facts, prices, events, metrics, etc. If context is insufficient, clearly say what information is missing. Separate facts from reasonable interpretation. 
			Watchlist-scoped context: 
			{joined}
			User Question: 
			{question}
			Answer with concise reasoning and cite context source labels
			"""