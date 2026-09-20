from app.db.database import SessionLocal
from ai_worker.consumer import consumer
from ai_worker.llm import generate
from app.logger import logger
from app.services.ai_service import AIService 
from app.services.rag_service import RAGService


# processing kafka message (contains just request_id)
def process_message(message: dict):
	request_id = message.get("request_id")
	db = SessionLocal()
	ai_service = AIService()
	try:
		# try to generate ai outcome
		request = ai_service.start_processing(db, request_id)
		if request is None:
			# missing request from the db
			return True
		user_id = request.user_id
		question = request.question
		context = RAGService().retrieve_context(db, user_id, question)
		# question + context => gives answer
		answer = generate(question, context)
		ai_service.mark_completed(db, request_id, answer)
		logger.info(f"AI request completed for reqID:{request_id}")
		return True
	except Exception:
		# failed to generate ai outcome
		logger.exception(f"AI request processing failed for reqID:{request_id}")
		try:
			ai_service.mark_failed(db, request_id)
			return True
		except Exception:
			# even failed to record failure
			db.rollback()
			logger.exception(f"AI request failure unable to persist for reqID:{request_id}")
			return False
	finally:
		db.close()


def main():
	logger.info("AI worker started")
	try:	
		# main kafka event loop
		for event in consumer:
			message = event.value
			if not process_message(message):
				# db didn't record its outcome
				raise TradeLabException("AI request outcome didn't persist")
			consumer.commit()
	finally:
		consumer.close()


if __name__ == "__main__":
	main()