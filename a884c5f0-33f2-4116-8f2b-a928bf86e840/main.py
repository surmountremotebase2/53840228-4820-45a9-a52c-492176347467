from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI
from surmount.data import SocialSentiment
from surmount.logging import log

class TradingStrategy(Strategy):

    def __init__(self):
        self.ticker = "SMCI"
        self.data_list = [SocialSentiment(self.ticker)]
        # Using RSI for momentum, and SocialSentiment for earnings expectation

    @property
    def interval(self):
        return "1day"
    
    @property
    def assets(self):
        return [self.ticker]

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        momentum = RSI(self.ticker, data["ohlcv"], length=14)
        sentiment = data[("social_sentiment", self.ticker)]
        smci_stake = 0

        if momentum and len(momentum) > 0:
            # Consider buying if RSI indicates strong upward momentum (i.e., not overbought)
            if momentum[-1] < 70:
                smci_stake = 1  # Fully invest in SMCI
            elif momentum[-1] > 70:
                # If RSI indicates overbought, might want to refrain from buying
                smci_stake = 0

        if sentiment and len(sentiment) > 0:
            latest_sentiment = sentiment[-1]
            # Looking at the latest available tweet and stocktwits sentiment
            if latest_sentiment["twitterSentiment"] < 0.5 or latest_sentiment["stocktwitsSentiment"] < 0.5:
                # If latest social sentiment is negative, consider it as an expectation of a bad earnings report
                smci_stake = 0  # Sell or avoid buying

        return TargetAllocation({self.ticker: smci_stake})