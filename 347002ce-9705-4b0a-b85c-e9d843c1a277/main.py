from surmount.base_class import Strategy, TargetAllocation
from surmount.data import OHLCV
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        # Example tickers, in a live scenario you would have a broader list or a method to fetch all tickers
        self.tickers = ["EXAMPLE1", "EXAMPLE2", "EXAMPLE3", "EXAMPLE4"]
        self.data_list = []

    @property
    def interval(self):
        # Using daily data for momentum calculation
        return "1day"

    @property
    def assets(self):
        # The assets we're interested in; in reality, this should be dynamically populated
        # with stocks below $1 from market data
        return self.tickers

    @property
    def data(self):
        # OHLCV data will be used for momentum calculation, not required to add here
        # as OHLCV is accessed directly via the self.ohlcv property in the run method
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            ohlcv_data = data["ohlcv"]
            if ticker not in ohlcv_data:
                continue  # Skip if no data

            prices = ohlcv_data[ticker]
            if len(prices) < 2:
                continue  # Need at least two days of data to compute momentum

            # Simplified momentum calculation: today's close vs previous close
            today_close = prices[-1]["close"]
            prev_close = prices[-2]["close"]

            # Filter for stocks below $1 and positive momentum
            if today_close < 1 and today_close > prev_close:
                allocation_dict[ticker] = 0.1  # Arbitrary allocation, adjust based on strategy needs

        # Normalize allocations if necessary to ensure total <= 1
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: weight / total_allocation for ticker, weight in allocation_dict.items()}

        return TargetAllocation(allocation_dict)