from collections import deque
from sortedcontainers import SortedList

# Order class representing a single buy or sell order
class Order:
    def __init__(self, id, order_type, side, price, quantity):
        # Validate input 
        if order_type not in ['limit', 'market']:
            raise ValueError('Order type must be limit or market')
        if side not in ['buy', 'sell']:
            raise ValueError('Side must be buy or sell')
        if not isinstance(price, float):
            raise ValueError('Price must be a float')
        
        self.id = id
        self.order_type = order_type
        self.side = side
        self.price = price
        self.quantity = quantity

# Trade class representing a successful trade between a buyer and a seller
class Trade:
    def __init__(self, buyer, seller, price, quantity):
        # Initialize trade attributes
        self.buy_order_id = buyer
        self.sell_order_id = seller
        self.price = price
        self.quantity = quantity

    def __str__(self):
    # Return a detailed string representation of the trade
        return (
        f"Trade executed: "
        f"Buyer Order ID: {self.buy_order_id}, "
        f"Seller Order ID: {self.sell_order_id}, "
        f"Price: {self.price}, "
        f"Quantity: {self.quantity} units"
        )


# OrderBook class that manages collections of buy (bids) and sell (asks) orders
class OrderBook:
    def __init__(self, bids=None, asks=None):
        # Initialize bids and asks as sorted lists
        # Bids are sorted in descending order of price (higher price first)
        # Asks are sorted in ascending order of price (lower price first)
        self.bids = SortedList(bids or [], key=lambda order: -order.price)
        self.asks = SortedList(asks or [], key=lambda order: order.price)

    def __len__(self):
        # Return the total number of orders in the order book
        return len(self.bids) + len(self.asks)

    def best_bid(self):
        # Return the highest bid price or 0 if no bids are available
        if len(self.bids) > 0:
            return self.bids[0].price
        return 0

    def best_ask(self):
        # Return the lowest ask price or 0 if no asks are available
        if len(self.asks) > 0:
            return self.asks[0].price
        return 0

    def add(self, order):
        # Add an order to the appropriate list (bids or asks)
        if order.side == 'buy':
            self.bids.add(order)
        elif order.side == 'sell':
            self.asks.add(order)

    def remove(self, order):
        # Remove an order from the appropriate list (bids or asks)
        try:
            if order.side == 'buy':
                self.bids.remove(order)
            elif order.side == 'sell':
                self.asks.remove(order)
        except ValueError:
            print(f"Order {order.id} not found in the order book")

# MatchingEngine class that processes orders and matches them to generate trades
class MatchingEngine:
    def __init__(self):
        # Initialize the order book and trade history
        self.queue = deque()
        self.orderbook = OrderBook()
        self.trades = deque()

    def process(self, order):
        # Market orders should be prioritized over limit orders.
        if order.order_type == "market":
            self.match_market_order(order)
        elif order.order_type == "limit":
            self.match_limit_order(order)

    def get_trades(self):
        # Return a list of all trades
        return list(self.trades)

    def match_limit_order(self, order):
        # Match a limit order by comparing it to existing orders in the order book
        if order.side == 'buy' and order.price >= self.orderbook.best_ask():
            # Buy order can be matched with existing asks
            self.match_order(order, self.orderbook.asks, is_bid=False)
        elif order.side == 'sell' and order.price <= self.orderbook.best_bid():
            # Sell order can be matched with existing bids
            self.match_order(order, self.orderbook.bids, is_bid=True)
        else:
            # Order cannot be matched immediately, so it is added to the order book
            self.orderbook.add(order)

    def match_market_order(self, order):
        # Match a market order by filling it with the best available prices
        if order.side == 'buy':
            self.match_order(order, self.orderbook.asks, is_bid=False)
        elif order.side == 'sell':
            self.match_order(order, self.orderbook.bids, is_bid=True)

    # match_order function does the actual matching
    # Core of this script
    def match_order(self, order, opposite_orders, is_bid):
        filled = 0
        consumed_orders = []

        for opposite_order in opposite_orders:
            # Market orders have no price constraint; limit orders should respect their price limit.
            if order.order_type == "limit":
                if (is_bid and opposite_order.price < order.price) or (not is_bid and opposite_order.price > order.price):
                    break  # Stop if the price is not favorable for a limit order

            # Determine the buyer and seller based on the order type
            if is_bid:
                buyer_id = opposite_order.id
                seller_id = order.id
            else:
                buyer_id = order.id
                seller_id = opposite_order.id

            # Fill as much of the order as possible
            if filled + opposite_order.quantity <= order.quantity:
                # order partially filled
                filled += opposite_order.quantity
                trade = Trade(buyer_id, seller_id, opposite_order.price, opposite_order.quantity)
                self.trades.append(trade)
                consumed_orders.append(opposite_order)
            else:
                # order completely filled
                volume = order.quantity - filled # calculates the amount that remains to be filled for this order
                filled += volume # update the filled
                trade = Trade(buyer_id, seller_id, opposite_order.price, volume)
                self.trades.append(trade)
                opposite_order.quantity -= volume
                if opposite_order.quantity == 0:
                    consumed_orders.append(opposite_order)
                break

        # Remove fully consumed orders from the order book
        for opposite_order in consumed_orders:
            self.orderbook.remove(opposite_order)

        # If the limit order wasn't fully filled, add the remainder back to the order book
        if order.order_type == "limit" and filled < order.quantity:
            self.orderbook.add(Order(order.id, "limit", order.side, order.price, order.quantity - filled))

        # market order that wasn't fully filled is discarded
