from fastapi import Request
from fastapi.responses import JSONResponse


# custom exception object for exception handling
class TradeLabException(Exception):
	def __init__(self, message: str, status_code: int = 400):
		self.message = message
		self.status_code = status_code


# type of exception that it handles => TradeLabException
async def tradelab_exception_handler(request: Request,
									exc: TradeLabException):
	return JSONResponse(status_code = exc.status_code,
						content = {
							"success": False,
							"error": exc.message
						})

# type of exception that it handles => Exception
async def generic_exception_handler(request: Request,
									exc: Exception):
	return JSONResponse(status_code = 500,
						content = {
							"success": False,
							"error": "Internal Server Error"
						})