"""investment_analysis.py - Mô-đun phân tích đầu tư tài chính"""

import yfinance as yf

def get_stock_price(symbol):
    """Lấy giá hiện tại của cổ phiếu theo mã."""
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")["Close"].iloc[-1]
        return f"📊 Giá hiện tại của {symbol.upper()} là {price:.2f} USD"
    except Exception as e:
        return f"❌ Lỗi khi lấy giá cổ phiếu {symbol}: {e}"

def get_crypto_price(coin_symbol):
    """Lấy giá tiền ảo từ Yahoo Finance (giới hạn coin phổ biến)."""
    crypto_map = {
        "BTC": "BTC-USD",
        "ETH": "ETH-USD",
        "BNB": "BNB-USD",
        "SOL": "SOL-USD",
        "DOGE": "DOGE-USD"
    }
    yf_symbol = crypto_map.get(coin_symbol.upper())
    if not yf_symbol:
        return f"⚠️ Không hỗ trợ coin {coin_symbol}."

    return get_stock_price(yf_symbol)

def compare_stocks(symbol1, symbol2):
    """So sánh giá giữa hai cổ phiếu."""
    try:
        stock1 = yf.Ticker(symbol1).history(period="1d")["Close"].iloc[-1]
        stock2 = yf.Ticker(symbol2).history(period="1d")["Close"].iloc[-1]
        diff = stock1 - stock2
        return f"{symbol1.upper()}: {stock1:.2f} USD, {symbol2.upper()}: {stock2:.2f} USD → Chênh lệch: {diff:.2f} USD"
    except Exception as e:
        return f"❌ Lỗi khi so sánh: {e}"

def suggest_investment(symbols=["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]):
    """Đề xuất đầu tư dựa trên xu hướng tăng trong 7 ngày qua."""
    suggestions = []
    for sym in symbols:
        try:
            stock = yf.Ticker(sym)
            hist = stock.history(period="7d")["Close"]
            if hist.iloc[-1] > hist.iloc[0]:
                diff = hist.iloc[-1] - hist.iloc[0]
                percent = diff / hist.iloc[0] * 100
                suggestions.append(f"{sym}: tăng {percent:.2f}% → NÊN xem xét")
        except Exception:
            continue

    if suggestions:
        return "🔍 Gợi ý đầu tư:\n" + "\n".join(suggestions)
    return "Hiện không có cổ phiếu nào tăng ổn định trong 7 ngày qua."