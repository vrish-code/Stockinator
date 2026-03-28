import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import animate as an

st.set_page_config(page_title="PSE Stock Simulator", layout="wide")

if "stock_dict" not in st.session_state:
    st.session_state.stock_dict = {
        "RELIANCE": {
            "Name": "Reliance Industries Limited",
            "Price": 21414.40,
            "Return Percentage 1 yr": 13.30,
            "6 month history": [20100.5, 20550.2, 20300.8, 20900.4, 21200.1, 21414.4],
        },
        "HDFCBANK": {
            "name": "HDFC Bank Limited",
            "Price": 20780.45,
            "Return Percentage 1 yr": -11.75,
            "history_6mo": [22500.0, 22100.4, 21800.6, 21200.3, 20950.8, 20780.45],
        },
        "TCS": {
            "Name": "Tata Consultancy Services Limited",
            "Price": 22390.60,
            "Return Percentage 1 yr": 1.41,
            "6 month history": [22100.2, 22250.5, 22050.1, 22400.9, 22300.4, 22390.6],
        },
        "ICICIBANK": {
            "Name": "ICICI Bank Limited",
            "Price": 21245.40,
            "Return Percentage 1 yr": 18.20,
            "6 month history": [18500.4, 19200.8, 19850.2, 20400.6, 20900.1, 21245.4],
        },
        "INFY": {
            "Name": "Infosys Limited",
            "Price": 21255.90,
            "Return Percentage 1 yr": 5.40,
            "6 month history": [20200.1, 20500.4, 20850.7, 21000.3, 21150.9, 21255.9],
        },
        "SBIN": {
            "Name": "State Bank of India",
            "Price": 21058.00,
            "Return Percentage 1 yr": 31.40,
            "6 month history": [16500.5, 17800.2, 18900.8, 19700.4, 20500.1, 21058.0],
        },
        "BHARTIARTL": {
            "Name": "Bharti Airtel Limited",
            "Price": 21846.10,
            "Return Percentage 1 yr": 42.10,
            "6 month history": [15800.2, 17200.5, 18500.1, 19900.9, 21000.4, 21846.1],
        },
    }

if "bought_stocks" not in st.session_state:
    st.session_state.bought_stocks = {}

if "sold_stocks" not in st.session_state:
    st.session_state.sold_stocks = {}

if "stock_df" not in st.session_state:
    df = pd.DataFrame.from_dict(st.session_state.stock_dict, orient="index")
    df.index.name = "ticker"
    st.session_state.stock_df = df.reset_index()


def buying_and_stats():
    tl = list(st.session_state.stock_dict.keys())
    pl = list(x["Price"] for x in st.session_state.stock_dict.values())
    c1, c2 = st.columns(2, border=True)
    with c1:
        st.subheader("Overview of stocks")
        st.dataframe(st.session_state.stock_df, hide_index=True)
        st.divider()
        f, a = plt.subplots()
        a.barh(tl, pl, color="green")
        a.grid(
            True, alpha=1.0, linewidth=0.9, linestyle="-", which="both", color="#fff"
        )
        a.set_xlim(0, 50000)
        a.set_title("Chart on prices of stocks")
        a.set_xlabel("Prices")
        a.set_ylabel("Tickers")
        st.pyplot(f)
        st.divider()
        st.caption("All prices in INR")
        st.divider()
        t1, t2, t3, t4, t5, t6, t7 = st.tabs(tl)
        with t1:
            st.line_chart(st.session_state.stock_dict[tl[0]].get("6 month history"))
        with t2:
            st.line_chart(st.session_state.stock_dict[tl[1]].get("6 month history"))
        with t3:
            st.line_chart(st.session_state.stock_dict[tl[2]].get("6 month history"))
        with t4:
            st.line_chart(st.session_state.stock_dict[tl[3]].get("6 month history"))
        with t5:
            st.line_chart(st.session_state.stock_dict[tl[4]].get("6 month history"))
        with t6:
            st.line_chart(st.session_state.stock_dict[tl[5]].get("6 month history"))
        with t7:
            st.line_chart(st.session_state.stock_dict[tl[6]].get("6 month history"))
    with c2:
        st.subheader("Buying market")
        st.divider()
        with st.form(key="Buying"):
            bsto = st.selectbox("Choose a stock to buy", tl)
            s = st.form_submit_button("Buy")
        if s:
            st.session_state.bought_stocks.append(
                {
                    "Ticker": tl.index(bsto),
                    "Data": st.session_state.stock_dict[bsto],
                }
            )
            an.animation.ani(bsto, True, False, True)
        st.divider()
        g, h = plt.subplots()
        g.set_facecolor = "#000"
        h.patch.set_facecolor = "#fff"
        h.barh(tl, retperasort, color="green")
        h.grid(True, alpha=1.0, linestyle="-", linewidth=0.9, which="both")
        h.set_title("Chart on stock with leading return percentage.")
        h.set_ylabel("Stocks")
        h.set_xlabel("Return percentages")
        h.set_ylim(0, max(retperasort))
        st.caption("All returns in INR")


def return_calc():
    with st.container(border=True):
        st.subheader("Return calculator")
        st.divider()
        stock_choice = st.selectbox(
            "Choose a stock", list(st.session_state.stock_dict.keys())
        )
        st.divider()
        noShares = st.number_input(
            "Choose the number of shares you want to buy", min=1, max=1000, step=1
        )
        st.divider()
        st.write(
            f"Return percentage for selected stock: {st.session_state.stock_dict[stock_choice]["Return percentage 1 yr"]}"
        )
        st.divider()
        ret_output = (st.session_state.stock_dict[stock_choice]["Price"] * noShares) * (
            st.session_state.stock_dict[stock_choice]["Return percentage 1 yr"] / 100
        )
        st.metric("Return output", f"₹{ret_output}")
        st.divider()


with st.sidebar:
    st.title("Sidebar")
    func = st.selectbox("Choose", ["Buying and stats", "Return calc"])
if func == "Buying and stats":
    buying_and_stats()
else:
    return_calc()
