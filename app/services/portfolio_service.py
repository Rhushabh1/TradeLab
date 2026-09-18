from sqlalchemy.orm import Session

from app.services.stock_service import StockService
# from app.cache.cache_service import cache 
from app.db.models import Portfolio, Transaction
from app.core.exceptions import TradeLabException


# just a simulation, not brokerage
# so no short selling, fractional shares, dividends, multi-currency, options, margin, market vs limit orders
class PortfolioService:
	def buy(self, db: Session, user_id: int, ticker: str, quantity: int):
		if quantity <= 0:
			raise TradeLabException("Quantity must be positive")
		ticker = ticker.strip().upper()
		stock = StockService().get_stock(db, ticker)
		price = stock["current_price"]
		holding = (db.query(Portfolio)
					.filter(Portfolio.user_id == user_id,
							Portfolio.ticker == ticker)
					.first())
		if holding:
			# update existing holding
			total_cost = (holding.quantity * holding.average_price)
			total_cost += quantity * price
			holding.quantity += quantity
			holding.average_price = total_cost/holding.quantity
		else:
			# create a new holding entry
			holding = Portfolio(user_id = user_id,
								ticker = ticker,
								quantity = quantity,
								average_price = price)
			db.add(holding)

		# update transaction table also
		db.add(Transaction(user_id = user_id,
							ticker = ticker,
							transaction_type = "BUY",
							quantity = quantity,
							price = price))
		db.commit()
		return holding

	def sell(self, db: Session, user_id: int, ticker: str, quantity: int):
		if quantity <= 0:
			raise TradeLabException("Quantity must be positive")
		ticker = ticker.strip().upper()
		holding = (db.query(Portfolio)
					.filter(Portfolio.user_id == user_id,
							Portfolio.ticker == ticker)
					# helps prevent concurrent sells (userful safeguard)
					.with_for_update()
					.first())
		if not holding or holding.quantity < quantity:
			raise TradeLabException("Insufficient quantity")
		stock = StockService().get_stock(db, ticker)
		price = stock["current_price"]
		transaction = Transaction(user_id = user_id,
								ticker = ticker,
								transaction_type = "SELL",
								quantity = quantity,
								price = price)
		db.add(transaction)
		remaining_quantity = holding.quantity - quantity
		if remaining_quantity == 0:
			db.delete(holding)
		else:
			holding.quantity = remaining_quantity
		try:
			db.commit()
			db.refresh(transaction)
		except Exception:
			db.rollback()
			raise
		return holding

	# for pnl data (never stored in db)
	# pnl calculated in service layer where persisted holdings meet live market data
	def summary(self, db: Session, user_id: int):
		holdings = (db.query(Portfolio)
					.filter(Portfolio.user_id == user_id)
					.all())
		result = []
		# loop can become expensive if StockService() makes a separate db request
		# TODO - optimize price retrieval later
		for holding in holdings:
			# fetch data about stock ticker
			stock = StockService().get_stock(db, holding.ticker)
			current = stock["current_price"]
			# compute pnl for each holding
			pnl = (current - holding.average_price) * holding.quantity
			result.append({
							"ticker": holding.ticker,
							"quantity": holding.quantity,
							"average_price": holding.average_price,
							"current_price": current,
							"pnl": round(pnl, 2)
							})
		return result

	# simply query the transaction table
	def transactions(self, db: Session, user_id: int):
		return (db.query(Transaction)
				.filter(Transaction.user_id == user_id)
				.all())