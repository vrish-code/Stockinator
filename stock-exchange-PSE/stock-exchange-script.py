import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import animate as an

plt.style.use("dark_background")
plt.rcParams.update(
    {
        "figure.facecolor": "#000000",
        "axes.facecolor": "#000000",
        "axes.edgecolor": "#FFFFFF",
        "grid.color": "#FFFFFF",
        "xtick.color": "#FFFFFF",
        "ytick.color": "#FFFFFF",
        "axes.labelcolor": "#FFFFFF",
        "text.color": "#FFFFFF",
        "lines.color": "#FFFFFF",
        "patch.edgecolor": "#FFFFFF",
    }
)

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
            "6 month history": [22500.0, 22100.4, 21800.6, 21200.3, 20950.8, 20780.45],
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
    st.session_state.bought_stocks = []

if "sold_stocks" not in st.session_state:
    st.session_state.sold_stocks = []

if "stock_df" not in st.session_state:
    df = pd.DataFrame.from_dict(st.session_state.stock_dict, orient="index")
    df.index.name = "ticker"
    st.session_state.stock_df = df.reset_index()


def buying_and_stats():
    tl = list(st.session_state.stock_dict.keys())
    pl = list(x["Price"] for x in st.session_state.stock_dict.values())
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Overview of stocks")
        st.divider()
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
        retpr = [
            abs(float(x["Return Percentage 1 yr"]))
            for x in st.session_state.stock_dict.values()
        ]
        retPerSort = list(sorted(retpr, reverse=True))
        g, h = plt.subplots()
        h.barh(tl, retPerSort, height=0.1, color="green")
        h.grid(True, alpha=1.0, linestyle="-", linewidth=0.9, which="both")
        h.set_title("Chart on stock with leading return percentage.")
        h.set_ylabel("Stocks")
        h.set_xlabel("Return percentages")
        h.set_xlim(0, max(retPerSort))
        st.pyplot(g)
        st.divider()
        st.caption("All returns in INR")
        st.divider()
        with st.form(key="Buying"):
            bsto = st.selectbox("Choose a stock to buy", tl)
            noS = st.number_input(
                "Choose the number of shares you want to buy", 1, 1000, 1
            )
            s = st.form_submit_button("Buy")
        if s:
            st.session_state.bought_stocks.append(
                {
                    "Ticker": tl[tl.index(bsto)],
                    "Name": st.session_state.stock_dict[bsto]["Name"],
                    "Price": st.session_state.stock_dict[bsto]["Price"],
                    "Return Percentage 1 yr": st.session_state.stock_dict[bsto][
                        "Return Percentage 1 yr"
                    ],
                    "6 month history": st.session_state.stock_dict[bsto][
                        "6 month history"
                    ],
                    "No of shares bought": noS,
                }
            )
            an.ani(True, True, False, bsto)


def return_calc():
    with st.container():
        st.subheader("Return calculator")
        st.divider()
        stock_choice = st.selectbox(
            "Choose a stock", list(st.session_state.stock_dict.keys())
        )
        st.divider()
        noShares = st.number_input(
            "Choose the number of shares you want to buy", 1, 1000, 1
        )
        st.divider()
        st.write(
            f"Return percentage (1 yr) for selected stock: {st.session_state.stock_dict[stock_choice]["Return Percentage 1 yr"]}"
        )
        st.divider()
        ret_output = (st.session_state.stock_dict[stock_choice]["Price"] * noShares) * (
            st.session_state.stock_dict[stock_choice]["Return Percentage 1 yr"] / 100
        )
        st.metric("Return output", f"₹{ret_output}")
        st.divider()


def portfolio_and_selling():
    st.subheader("Portfolio")
    st.divider()
    tl = list(st.session_state.stock_dict.keys())
    with st.container():
        st.subheader("View the stocks you bought")
        st.divider()
        boughtStocksDf = pd.DataFrame(st.session_state.bought_stocks)
        st.dataframe(boughtStocksDf)
        st.divider()
    with st.container():
        st.subheader("Total investement money")
        st.divider()
        totalInvVar: float = 0.0
        for l in range(len(st.session_state.bought_stocks)):
            totalInvVar += (
                st.session_state.bought_stocks[l]["Price"]
                * st.session_state.bought_stocks[l]["No of shares bought"]
            )
        st.metric("Total investment in INR", totalInvVar)
        st.divider()
        st.subheader("Percentage of money in each stock")

        pctInvinEachStock = []
        for o in range(len(st.session_state.bought_stocks)):
            pctInvinEachStock.append(
                {
                    st.session_state.bought_stocks[o]["Ticker"]: (
                        (
                            st.session_state.bought_stocks[o]["Price"]
                            * st.session_state.bought_stocks[o]["No of shares bought"]
                        )
                        / totalInvVar
                    )
                    * 100
                }
            )
        pctInv = []
        for g in range(len(st.session_state.bought_stocks)):
            (
                (
                    st.session_state.bought_stocks[g]["Price"]
                    * st.session_state.bought_stocks[g]["No of shares bought"]
                )
                / totalInvVar
            ) * 100
        pctInvDfj = pd.json_normalize(pctInvinEachStock)
        pctInvDf = pd.DataFrame(pctInvDfj)
        h, p = plt.subplots()
        p.barh(tl, pctInv, color="green")
        p.grid(
            True, alpha=0.06, linestyle="-", linewidth=0.1, which="both", axis="both"
        )
        p.set_title(f"Percentages of total amount ({totalInvVar}) invested in stocks")
        p.set_xlabel("Percentage")
        p.set_ylabel("Tickers")
        p.set_xlim(0, 100)
        st.pyplot(h)


st.sidebar.title("Basic")
c = st.sidebar.selectbox("Choose", ["Buying and stats", "Portfolio and selling"])
if c == "Buying and stats":
    buying_and_stats()
else:
    portfolio_and_selling()
