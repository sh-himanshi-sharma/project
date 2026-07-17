# tool/stock.py
import requests
import yfinance as yf
from datetime import datetime, timedelta

def execute(arguments: dict):
    """
    Fetch real-time stock data for any company
    """
    symbol = arguments.get("symbol")
    action = arguments.get("action", "price")  # price, info, history, quote
    
    if not symbol:
        return "Stock error: No stock symbol provided"
    
    try:
        # Create ticker object
        ticker = yf.Ticker(symbol)
        
        # Get current data
        info = ticker.info
        
        if action == "price":
            # Get current price
            current_price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            previous_close = info.get("previousClose", "N/A")
            change = current_price - previous_close if current_price != "N/A" and previous_close != "N/A" else "N/A"
            change_percent = (change / previous_close * 100) if change != "N/A" and previous_close != "N/A" else "N/A"
            
            return (
                f"📊 Stock: {symbol.upper()}\n"
                f"💰 Current Price: ${current_price}\n"
                f"📈 Previous Close: ${previous_close}\n"
                f"📉 Change: ${change:.2f} ({change_percent:.2f}%)" if change != "N/A" else ""
            )
            
        elif action == "info":
            # Get full company info
            name = info.get("longName", info.get("shortName", "N/A"))
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")
            market_cap = info.get("marketCap", "N/A")
            if market_cap != "N/A":
                market_cap = f"${market_cap:,.0f}"
            
            pe_ratio = info.get("trailingPE", "N/A")
            eps = info.get("trailingEps", "N/A")
            dividend_yield = info.get("dividendYield", "N/A")
            if dividend_yield != "N/A":
                dividend_yield = f"{dividend_yield * 100:.2f}%"
            
            return (
                f"📊 {name} ({symbol.upper()})\n"
                f"{'='*40}\n"
                f"🏭 Sector: {sector}\n"
                f"📋 Industry: {industry}\n"
                f"💰 Market Cap: {market_cap}\n"
                f"📈 P/E Ratio: {pe_ratio}\n"
                f"💵 EPS: ${eps}\n"
                f"💸 Dividend Yield: {dividend_yield}"
            )
            
        elif action == "history":
            # Get historical data
            period = arguments.get("period", "1mo")  # 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
            hist = ticker.history(period=period)
            
            if hist.empty:
                return f"No historical data found for {symbol}"
            
            latest = hist.iloc[-1]
            first = hist.iloc[0]
            
            high = hist['High'].max()
            low = hist['Low'].min()
            avg = hist['Close'].mean()
            
            return (
                f"📊 {symbol.upper()} - Historical Data ({period})\n"
                f"{'='*40}\n"
                f"📈 Current: ${latest['Close']:.2f}\n"
                f"📊 Period High: ${high:.2f}\n"
                f"📉 Period Low: ${low:.2f}\n"
                f"📊 Average: ${avg:.2f}\n"
                f"📈 Volume: {latest['Volume']:,.0f}\n"
                f"📅 Period: {first.name.strftime('%d-%m-%Y')} to {latest.name.strftime('%d-%m-%Y')}"
            )
            
        elif action == "quote":
            # Get quote summary
            # Get current data
            current_price = info.get("currentPrice", info.get("regularMarketPrice", "N/A"))
            day_high = info.get("dayHigh", "N/A")
            day_low = info.get("dayLow", "N/A")
            volume = info.get("volume", "N/A")
            avg_volume = info.get("averageVolume", "N/A")
            
            return (
                f"📊 Quote: {symbol.upper()}\n"
                f"{'='*40}\n"
                f"💰 Current: ${current_price}\n"
                f"📈 Day High: ${day_high}\n"
                f"📉 Day Low: ${day_low}\n"
                f"📊 Volume: {volume:,}\n"
                f"📊 Avg Volume: {avg_volume:,}"
            )
        
        else:
            return f"Unknown action: {action}. Use: price, info, history, quote"
            
    except Exception as e:
        return f"Stock error: {e}. Check if symbol '{symbol}' is valid."

def get_multiple_stocks(symbols: list):
    """Get prices for multiple stocks"""
    results = []
    for symbol in symbols:
        result = execute({"symbol": symbol, "action": "price"})
        results.append(result)
    return "\n\n".join(results)

if __name__ == "__main__":
    print("Stock Tool Testing")
    print("="*60)
    
    # Test with different symbols
    test_symbols = ["AAPL", "TSLA", "GOOGL", "MSFT"]
    
    for symbol in test_symbols:
        print(f"\nTesting: {symbol}")
        print("-"*40)
        result = execute({"symbol": symbol, "action": "price"})
        print(result)