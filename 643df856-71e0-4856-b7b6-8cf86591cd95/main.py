from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log
from surmount.data import OHLCV

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["EXAMPLE"]  # Placeholder for ticker(s)
        self.data_list = []  # Assuming data_list is populated elsewhere with OHLCV data

    @property
    def interval(self):
        return "1day"  # Daily interval for SMA calculation

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Check if we have enough data points for the longest SMA calculation
            if len(data["ohlcv"]) < 100:
                log(f"Not enough data for {ticker}.")
                continue

            current_price = data["ohlcv"][-1][ticker]["close"]
            # Filter for stocks below $1
            if current_price >= 1:
                log(f"{ticker} is above $1 threshold.")
                continue

            sma30 = SMA(ticker, data["ohlcv"], 30)
            sma100 = SMA(ticker, data["ohlcv"], 100)
            
            if sma30 is None or sma100 is None:
                log("SMA calculation failed.")
                continue

            # Check if the 30-day SMA has crossed above the 100-day SMA
            if sma30[-1] > sma100[-1] and sma30[-2] <= sma100[-2]:
                log(f"Buying signal for {ticker}.")
                allocation_dict[ticker] = 1.0  # Full allocation
            else:
                log(f"No action for {ticker}.")
                allocation_dict[ticker] = 0.0  # No allocation

        return TargetAllocation(allocation_dict)