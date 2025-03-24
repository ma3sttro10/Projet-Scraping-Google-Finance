import requests as r
from bs4 import BeautifulSoup as bs
from dataclasses import dataclass
from tabulate import tabulate
# https://www.google.com/finance/quote/GOOGL:NASDAQ
@dataclass
class Stock:
    ticker : str
    exchange: str
    price: float = 0
    currency: str = "USD"
    def __post_init__(self):
        price_info = get_price(self.ticker,self.exchange)
        if price_info["ticker"] == self.ticker:
            self.price = price_info["Price"]
            self.currency = price_info["Currency"]

# ------------------------ Position------
@dataclass
class Position:
    stock : Stock
    Quantity : int = 0
# ------------------------ Portfolio------

@dataclass
class Portfolio:
    positions : list[Position]

    def get_total_value(self):
        total_value = 0
        for position in self.positions:
            total_value += position.Quantity * position.stock.price
        return total_value


def get_exchange(currency):
    url = f"https://www.google.com/finance/quote/{currency}-USD"
    resp = r.get(url)
    soup = bs(resp.content, "html.parser")
    price_div = soup.find("div",attrs={"data-last-price": True})["data-last-price"]
    return float(price_div)
def get_price(ticker,exchange):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    response = r.get(url)
    soup = bs(response.content,"html.parser")
    price_div = soup.find("div",attrs={"data-last-price":True})
    price = float(price_div["data-last-price"])
    currency = price_div["data-currency-code"]
    if currency != "USD" :
        exchanger = get_exchange(currency)
        price = price * exchanger
        currency = "USD"
    return {"ticker":ticker,"Exchange":exchange,"Price": round(price,2),"Currency":currency}
def display_portfolio(portfolio):
    if not isinstance(portfolio,Portfolio):
        raise TypeError("Please Provide an instance of type Portfolio")
    portfolio_value = portfolio.get_total_value()
    position_data = []
    for position in sorted(portfolio.positions,key=lambda x: x.Quantity,reverse=True):
        position_data.append([position.stock.ticker,position.stock.exchange,position.Quantity,position.stock.price,position.Quantity*position.stock.price,
                              position.Quantity*position.stock.price/portfolio_value * 100])
    print(tabulate(position_data,headers=["Tickers","Exchange","Quantity","Price","Total Market Value","% Allocation"],
                   tablefmt="psql",floatfmt=".2f"))
    print("Total Portfolio Value = ",portfolio_value)

if __name__ == "__main__":
    Shopify = Stock("SHOP","TSE")
    Amazon = Stock("AMZN","NASDAQ")
    Microsoft = Stock("MSFT","NASDAQ")
    Google = Stock("GOOGL","NASDAQ")
    portf = Portfolio([Position(Google,30),Position(Shopify,10),Position(Microsoft,2),Position(Amazon,25)])
    display_portfolio(portf)