import pyotp
import streamlit as st
import pandas as pd
from SmartApi import SmartConnect  # or from SmartApi.smartConnect import SmartConnect

st.set_page_config(layout="wide")

html_code = """
<!-- TradingView Widget BEGIN -->
<div class="tradingview-widget-container">
  <div class="tradingview-widget-container__widget"></div>
  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"></a></div>
  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>
  {
  "width": "1315",
  "height": "635",
  "symbol": "BSE:SENSEX",
  "interval": "D",
  "timezone": "Etc/UTC",
  "theme": "dark",
  "style": "1",
  "locale": "en",
  "allow_symbol_change": true,
  "calendar": false,
  "support_host": "https://www.tradingview.com"
}
  </script>
</div>
<!-- TradingView Widget END -->
"""

st.components.html(html_code, height=650, width=1330)

api_key = 'dIiTULVm'
username = 'IIRA13264'
pwd = '0706'
smartApi = SmartConnect(api_key)

try:
    token = "CLOJB3JKRWDLM227PRTMCAVCMQ"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    st.error("Invalid Token: The provided token is not valid.")
    raise e

correlation_id = "abcde"
try:
    data = smartApi.generateSession(username, pwd, totp)
except Exception as e:
    st.error(f"Error generating session: {e}")
    data = None

if data and data.get('status') == False:
    st.error(data)
else:
    if data:
        try:
            authToken = data['data']['jwtToken']
            refreshToken = data['data']['refreshToken']
            feedToken = smartApi.getfeedToken()
            res = smartApi.getProfile(refreshToken)
            smartApi.generateToken(refreshToken)
            res = res['data']['exchanges']
        except Exception as e:
            st.error(f"Error during API interactions: {e}")
            res = None

    st.title("Order Placement App")

    variety = st.selectbox("Variety", ["NORMAL"])
    tradingsymbol = st.text_input("Trading Symbol")
    symboltoken = st.text_input("Symbol Token")
    transactiontype = st.selectbox("Transaction Type", ["BUY", "SELL"])
    exchange = st.selectbox("Exchange", ["NSE", "BSE"])
    ordertype = st.selectbox("Order Type", ["LIMIT", "MARKET"])
    producttype = st.selectbox("Product Type", ["INTRADAY", "DELIVERY"])
    duration = st.selectbox("Duration", ["DAY"])
    price = st.number_input("Price")
    squareoff = st.number_input("Squareoff")
    stoploss = st.number_input("Stoploss")
    quantity = st.number_input("Quantity")

    orderparams = {
        "variety": variety,
        "tradingsymbol": tradingsymbol,
        "symboltoken": symboltoken,
        "transactiontype": transactiontype,
        "exchange": exchange,
        "ordertype": ordertype,
        "producttype": producttype,
        "duration": duration,
        "price": price,
        "squareoff": squareoff,
        "stoploss": stoploss,
        "quantity": quantity
    }

    # Place order when button is clicked
    if st.button("Place Order"):
        try:
            orderid = smartApi.placeOrder(orderparams)
            st.success(f"Order placed successfully with Order ID: {orderid}")
            order_df = pd.DataFrame([{
                "Order ID": orderid,
                "Trading Symbol": tradingsymbol,
                "Transaction Type": transactiontype,
                "Quantity": quantity,
                "Price": price
            }])
            st.write("### Last Order Placed")
            st.dataframe(order_df)
        except Exception as e:
            st.error(f"Order placement failed: {e}")
