from TradeMatching import Order, OrderBook, MatchingEngine

# Create a list of sample orders
orders = [
    Order(1, 'limit', 'sell', 105.0, 5),  # Sell 5 units at $105.00
    Order(2, 'limit', 'sell', 110.0, 3),  # Sell 3 units at $110.00
    Order(3, 'limit', 'buy', 100.0, 4),   # Buy 4 units at $100.00
    Order(4, 'market', 'buy', 0.0, 6),    # Buy 6 units at market price
    Order(5, 'limit', 'buy', 107.0, 2),   # Buy 2 units at $107.00
    Order(6, 'market', 'sell', 0.0, 4),   # Sell 4 units at market price
    Order(7, 'limit', 'sell', 108.0, 1),  # Sell 1 unit at $108.00
    Order(8, 'limit', 'buy', 109.0, 3)    # Buy 3 units at $109.00
]


# Initialize the order book and matching engine
order_book = OrderBook()
matching_machine = MatchingEngine()

# Process each order through the matching engine
for order in orders:
    matching_machine.process(order)

# Retrieve and print all trades that occurred
trades = matching_machine.get_trades()
for trade in trades:
    print(trade)

print('Finished processing orders')
