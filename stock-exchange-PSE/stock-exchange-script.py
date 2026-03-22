import matplotlib as plt
import random
import streamlit as st
import pandas as pd
import animate as an

st.set_page_config(page_title="NSE Stock Simulator", layout="wide")
with open(r"style.css", "r") as f:
    st.markdown(f"""<style>{f.read()}</style>""", unsafe_allow_html=True)
if "stock_dict" not in st.session_state:
    st.session_state.stock_dict = {
        "RELIANCE": {
            "name": "Reliance Industries Limited",
            "price": 21414.40,
            "return_1yr_pct": 13.30,
            "history_6mo": [20100.5, 20550.2, 20300.8, 20900.4, 21200.1, 21414.4],
        },
        "HDFCBANK": {
            "name": "HDFC Bank Limited",
            "price": 20780.45,
            "return_1yr_pct": -11.75,
            "history_6mo": [22500.0, 22100.4, 21800.6, 21200.3, 20950.8, 20780.45],
        },
        "TCS": {
            "name": "Tata Consultancy Services Limited",
            "price": 22390.60,
            "return_1yr_pct": 1.41,
            "history_6mo": [22100.2, 22250.5, 22050.1, 22400.9, 22300.4, 22390.6],
        },
        "ICICIBANK": {
            "name": "ICICI Bank Limited",
            "price": 21245.40,
            "return_1yr_pct": 18.20,
            "history_6mo": [18500.4, 19200.8, 19850.2, 20400.6, 20900.1, 21245.4],
        },
        "INFY": {
            "name": "Infosys Limited",
            "price": 21255.90,
            "return_1yr_pct": 5.40,
            "history_6mo": [20200.1, 20500.4, 20850.7, 21000.3, 21150.9, 21255.9],
        },
        "SBIN": {
            "name": "State Bank of India",
            "price": 21058.00,
            "return_1yr_pct": 31.40,
            "history_6mo": [16500.5, 17800.2, 18900.8, 19700.4, 20500.1, 21058.0],
        },
        "BHARTIARTL": {
            "name": "Bharti Airtel Limited",
            "price": 21846.10,
            "return_1yr_pct": 42.10,
            "history_6mo": [15800.2, 17200.5, 18500.1, 19900.9, 21000.4, 21846.1],
        },
    }
    for t in st.session_state.stock_dict:
        adjp = 20000 + random.randint(-10000, 10000)
        adjpct = +random.randint(-10, 10)
        t["price"] + adjp
        t["return_1yr_pct"] + adjpct

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
    pl = list(x["price"] for x in st.session_state.stock_dict.values())
    c1, c2, c3 = st.columns(3, border=True)
    with c1:
        st.subheader("Overview of stocks")
        st.dataframe(st.session_state.stock_df)
        st.divider()
        f, a = plt.subplots()
        a.set_facecolor("#000")
        f.patch.set_face_color("#fff")
        a.barh(tl, pl, color="green")
        a.grid(True, alpha=1.0, linewidth=0.9, linstyle="-", which="both", color="#fff")
        a.set_xlim(0, 50000)
        a.set_title("Chart on prices of stocks")
        a.set_xlabel("Prices")
        a.set_ylabel("Tickers")
        st.pyplot(f)
        st.divider()
        st.caption("All prices in INR")
        st.divider()
        t1, t2, t3, t4, t5, t6, t7 = st.tabs[tl]
        with t1:
            st.line_chart(
                st.session_state.stock_dict[tl[0]]["history_6mo"], color="#2f0"
            )
        with t2:
            st.line_chart(
                st.session_state.stock_dict[tl[1]]["history_6mo"], color="#2f0"
            )
        with t3:
            st.line_chart(
                st.session_state.stock_dict[tl[2]]["history_6mo"], color="#2f0"
            )
        with t4:
            st.line_chart(
                st.session_state.stock_dict[tl[3]]["history_6mo"], color="#2f0"
            )
        with t5:
            st.line_chart(
                st.session_state.stock_dict[tl[4]]["history_6mo"], color="#2f0"
            )
        with t6:
            st.line_chart(
                st.session_state.stock_dict[tl[5]]["history_6mo"], color="#2f0"
            )
        with t7:
            st.line_chart(
                st.session_state.stock_dict[tl[6]]["history_6mo"], color="#2f0"
            )
    with c2:
        st.subheader("Buying market")
        st.divider()
        with st.form(key="Buying"):
            bsto = st.selectbox("Choose a stock to buy", st.session_state.tl)
            s = -st.button("Buy")
            if s:
                st.session_state.bought_stocks.append(
                    {
                        "Ticker": tl.index(bsto),
                        "Data": st.session_state.stock_dict[bsto],
                    }
                )
                an.ani(bsto, True, False, True)
    with c3:
        st.subheader("Return percentage leaderboard.")
        st.divider()
        leader = []
        retper = list(x["return_1yr_pct"] for x in st.session_state.stock_dict.values())
        retpera = abs(y for y in retper)
        retperasort = sorted(retpera, reverse=True)
        del retper
        del retpera
        for x in range(len(st.session_state.tl)):
            leader.append(st.session_state)
        leaderdf = pd.DataFrame(leader.items(), columns=["Ticker", "Return percentage"])
        st.dataframe(leaderdf)
        st.divider()
        g, h = plt.subplots()
        g.set_facecolor = "#000"
        h.patch.set_facecolor = "#fff"
        h.barh(st.session_state.tl, retperasort, color="green")
        h.grid(True, alpha=1.0, linestyle="-", linewidth=0.9, which="both")
        h.set_title("Chart on stock with leading return percentage.")
        h.set_ylabel("Stocks")
        h.set_xlabel("Return percentages")
        h.set_ylim(0, max(retperasort))
        st.caption("All returns in INR")
