The Python scripts implement a simple trade matching engine for a financial exchange. The core functionality revolves around managing and matching buy and sell orders based on predefined rules. The system includes classes for handling both limit and market orders, managing an order book, and processing trades.

```TradeMatching.py```: This script defines the main components of the trade matching system, including the Order, Trade, OrderBook, and MatchingEngine classes. The OrderBook manages the lists of buy (bid) and sell (ask) orders, while the MatchingEngine processes incoming orders to match them against existing orders in the order book.

```test.py```: This script creates a few example orders, adds them to the order book, and then uses the MatchingEngine to process these orders, attempting to match them against each other.
