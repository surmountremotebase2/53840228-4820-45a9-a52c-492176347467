from surmount.base_class import Strategy, TargetAllocation
from surmount.data import CboeVolatilityIndexVix

class TradingStrategy(Strategy):
    def __init__(self):
        # Define the ticker for Apple Inc.
        self.tickers = ["AAPL"]
        
        # Add the VIX to our data list for monitoring
        self.data_list = [CboeVolatilityIndexVix()]

    @property
    def interval(self):
        # Define the interval for checking - "1day" for daily volatility checks
        return "1day"

    @property
    def assets(self):
        # Return the list of assets to trade - in this case, just AAPL
        return self.tickers

    @property
    def data(self):
        # Return the data subscription list, including VIX data
        return self.data_list

    def run(self, data):
        # Allocate 0% initially
        allocation_dict = {"AAPL": 0}
        
        # Access VIX values from the data dictionary using the defined access key
        vix_data = data[("cboe_volatility_index_vix",)]
        
        # Check if we have VIX data
        if vix_data and len(vix_data) > 0:
            latest_vix_value = vix_data[-1]['value']
            
            # If VIX is greater than 30, consider it 'high' and allocate a percentage to AAPL
            if latest_vix_value > 30:
                allocation_dict["AAPL"] = 0.1  # For example, allocate 10% to AAPL, adjust as needed
        
        # Return the target allocation
        return TargetAllocation(allocation_dict)

    # Note: It's crucial to consider implementing safety checks and a more nuanced allocation logic
    # depending on the broader investment strategy and risk management rules.