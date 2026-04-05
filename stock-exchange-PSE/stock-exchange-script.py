import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import animate as an


st.set_page_config(
    page_title="PSE Stock Simulator", layout="wide", initial_sidebar_state="expanded"
)

plt.style.use("dark_background")
plt.rcParams.update(
    {
        "figure.facecolor": "#002b36",
        "axes.facecolor": "#073642",
        "axes.edgecolor": "#586e75",
        "grid.color": "#586e75",
        "xtick.color": "#839496",
        "ytick.color": "#839496",
        "axes.labelcolor": "#839496",
        "text.color": "#839496",
        "lines.color": "#268bd2",
        "patch.edgecolor": "#839496",
    }
)

if "bank_account" not in st.session_state:
    st.session_state.bank_account: float = 0.0
if "stock_dict" not in st.session_state:
    st.session_state.stock_dict = {
        "RELIANCE": {
            "Name": "Reliance Industries Limited",
            "Price (1 share)": 21414.40 + random.randint(100, 100000),
            "Return Percentage 1 yr": 13.30 - random.randint(-10, 10),
            "6 month history": [20100.5, 20550.2, 20300.8, 20900.4, 21200.1, 21414.4],
        },
        "HDFCBANK": {
            "Name": "HDFC Bank Limited",
            "Price (1 share)": 20780.45 - random.randint(100, 100000),
            "Return Percentage 1 yr": -11.75 + random.randint(-10, 10),
            "6 month history": [22500.0, 22100.4, 21800.6, 21200.3, 20950.8, 20780.45],
        },
        "TCS": {
            "Name": "Tata Consultancy Services Limited",
            "Price (1 share)": 22390.60 + random.randint(100, 100000),
            "Return Percentage 1 yr": 1.41 - random.randint(-10, 10),
            "6 month history": [22100.2, 22250.5, 22050.1, 22400.9, 22300.4, 22390.6],
        },
        "ICICIBANK": {
            "Name": "ICICI Bank Limited",
            "Price (1 share)": 21245.40 - random.randint(100, 100000),
            "Return Percentage 1 yr": 18.20 + random.randint(-10, 10),
            "6 month history": [18500.4, 19200.8, 19850.2, 20400.6, 20900.1, 21245.4],
        },
        "INFY": {
            "Name": "Infosys Limited",
            "Price (1 share)": 21255.90 + random.randint(100, 100000),
            "Return Percentage 1 yr": 5.40 - random.randint(-10, 10),
            "6 month history": [20200.1, 20500.4, 20850.7, 21000.3, 21150.9, 21255.9],
        },
        "SBIN": {
            "Name": "State Bank of India",
            "Price (1 share)": 21058.00 - random.randint(100, 100000),
            "Return Percentage 1 yr": 31.40 + random.randint(-10, 10),
            "6 month history": [16500.5, 17800.2, 18900.8, 19700.4, 20500.1, 21058.0],
        },
        "BHARTIARTL": {
            "Name": "Bharti Airtel Limited",
            "Price (1 share)": 21846.10 + random.randint(100, 100000),
            "Return Percentage 1 yr": 42.10 - random.randint(-10, 10),
            "6 month history": [15800.2, 17200.5, 18500.1, 19900.9, 21000.4, 21846.1],
        },
    }

if "bought_stocks" not in st.session_state:
    st.session_state.bought_stocks = []

if "sold_stocks" not in st.session_state:
    st.session_state.sold_stocks = []

if "stock_df" not in st.session_state:
    df = pd.DataFrame.from_dict(st.session_state.stock_dict, orient="index")
    df.index.name = "Ticker"
    st.session_state.stock_df = df.reset_index()


def buying_and_stats():
    tl = list(st.session_state.stock_dict.keys())
    pl = list(x["Price (1 share)"] for x in st.session_state.stock_dict.values())
    c1, c2 = st.columns([4, 3])
    with c1:
        st.subheader("Overview of stocks")
        st.divider()
        st.dataframe(st.session_state.stock_df, hide_index=True)
        st.divider()
        f, a = plt.subplots()
        a.barh(tl, pl, color="#00FFFF")
        a.grid(
            True, alpha=1.0, linewidth=0.5, linestyle="-", which="both", color="#fff"
        )
        a.set_xlim(0, 50000)
        a.set_title("Chart on prices of stocks")
        a.set_xlabel("Prices")
        a.set_ylabel("Tickers")
        st.pyplot(f)
        st.divider()
        st.caption("All prices in INR")
        st.divider()

    with c2:
        st.subheader("Buying market")
        st.divider()
        retpr = [
            float(x["Return Percentage 1 yr"])
            for x in st.session_state.stock_dict.values()
        ]
        retPerSort = list(sorted(retpr, reverse=True))
        g, h = plt.subplots()
        h.barh(
            sorted(
                list(st.session_state.stock_dict.keys()),
                key=lambda k: st.session_state.stock_dict[k]["Return Percentage 1 yr"],
                reverse=True,
            ),
            retPerSort,
            height=0.1,
            color="#00FFFF",
        )
        h.grid(
            True,
            which="both",
            axis="both",
            alpha=1.0,
            linewidth=0.8,
            linestyle="-",
            aa=True,
            color="#fff",
        )
        h.set_title("Chart on stock with leading return percentage.")
        h.set_ylabel("Stocks")
        h.set_xlabel("Return percentages")
        h.set_xlim(min(retPerSort), max(retPerSort))
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
            st.warning(
                "Do not click the same stock on the dropdown and the buy button twice or more."
            )
        if s:
            st.session_state.bought_stocks.append(
                {
                    "Ticker": tl[tl.index(bsto)],
                    "Name": st.session_state.stock_dict[bsto]["Name"],
                    "Price (1 share)": st.session_state.stock_dict[bsto][
                        "Price (1 share)"
                    ],
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

    with st.container():
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
        ret_output = (
            st.session_state.stock_dict[stock_choice]["Price (1 share)"] * noShares
        ) * (st.session_state.stock_dict[stock_choice]["Return Percentage 1 yr"] / 100)
        st.metric("Return output", f"₹{ret_output}")
        st.divider()


def portfolio_and_selling():
    st.header("Portfolio")
    st.divider()
    totInv = float(
        sum(
            st.session_state.bought_stocks[a]["Price (1 share)"]
            for a in range(len(st.session_state.bought_stocks))
        )
        * sum(
            st.session_state.bought_stocks[b]["No of shares bought"]
            for b in range(len(st.session_state.bought_stocks))
        )
    )
    totPL = totInv - sum(
        st.session_state.bought_stocks[o]["Price (1 share)"]
        for o in range(len(st.session_state.bought_stocks))
    )
    with st.container(key="overview_data"):
        c1, c2 = st.columns(2, gap="large")
        with c1:
            with st.expander("Total investement made"):
                st.metric("Total investment", f"{totInv:.2f} INR")
            with st.expander("Total profit/loss"):
                st.metric(
                    "Total P/L", f"{totPL:.2f} INR", f"{totPL / totInv * 100:.2f}%"
                )
        with c2:
            with st.expander("Total returns"):
                tabs = st.tabs(
                    list(
                        st.session_state.bought_stocks[p].get("Ticker")
                        for p in range(len(st.session_state.bought_stocks))
                    )
                )
                for o, p in enumerate(tabs):
                    with p:
                        st.metric(
                            f"{st.session_state.bought_stocks[o]["Ticker"]}",
                            f"{st.session_state.bought_stocks[o]["Return Percentage 1 yr"]*st.session_state.bought_stocks[o]["No of shares bought"]:.2f}%",
                        )
            with st.expander("Total shares bought for each stock"):
                tabs = st.tabs(
                    list(
                        st.session_state.bought_stocks[p].get("Ticker")
                        for p in range(len(st.session_state.bought_stocks))
                    )
                )
                for i, t in enumerate(tabs):
                    with t:
                        st.metric(
                            f"No of shares bought for {st.session_state.bought_stocks[i]["Ticker"]}",
                            st.session_state.bought_stocks[i]["No of shares bought"],
                        )
    st.divider()
    with st.container(key="portWeight"):
        poWeightDict = {}
        for y in range(len(st.session_state.bought_stocks)):
            poWeightDict[st.session_state.bought_stocks[y]["Ticker"]] = round(
                (
                    st.session_state.bought_stocks[y]["Price (1 share)"]
                    * st.session_state.bought_stocks[y]["No of shares bought"]
                    / totInv
                    * 100
                ),
                2,
            )

        poWeightDf = pd.DataFrame(
            list(poWeightDict.items()), columns=["Tickers", "Share owned in portfolio"]
        )
        st.dataframe(poWeightDf, hide_index=True)

        j, k = plt.subplots()
        k.barh(
            list(poWeightDict.keys()),
            list(poWeightDict.values()),
            height=0.3,
            color="#00FFFF",
        )
        k.grid(
            True,
            which="both",
            axis="both",
            alpha=1.0,
            linewidth=0.8,
            linestyle="-",
            aa=True,
            color="#fff",
        )
        k.set_xlim(0, 100)
        k.set_xlabel("Percentages of portfolio owned")
        k.set_ylabel("Stocks owned")
        st.pyplot(j)
    c1, c2, c3 = st.columns(3)


with st.sidebar:
    st.title("haha")
    s = st.selectbox("Choose", ["1", "2"])
if s == "1":
    buying_and_stats()
else:
    portfolio_and_selling()
