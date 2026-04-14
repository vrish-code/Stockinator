import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import animate as an
import requests as r

st.set_page_config(
    page_title="PSE Stock Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

plt.style.use("dark_background")
plt.rcParams.update(
    {
        "figure.facecolor": "#0b0f14",
        "axes.facecolor": "#121821",
        "axes.edgecolor": "#2a3441",
        "grid.color": "#2f3b4a",
        "xtick.color": "#aab4c3",
        "ytick.color": "#aab4c3",
        "axes.labelcolor": "#cbd5e1",
        "text.color": "#e2e8f0",
        "patch.edgecolor": "#2a3441",
        "axes.titleweight": "semibold",
        "axes.titlesize": 14,
    }
)

if "stock_dict" not in st.session_state:
    st.session_state.stock_dict = {
        "RELIANCE": {
            "Name": "Reliance Industries Limited",
            "Price (1 share)": 21414.40 + random.randint(100, 100000),
            "Return Percentage 1 yr": 13.30 - random.randint(-10, 10),
            "6 month history": [
                20100.5,
                20550.2,
                20300.8,
                20900.4,
                21200.1,
                21414.4,
            ],
        },
        "HDFCBANK": {
            "Name": "HDFC Bank Limited",
            "Price (1 share)": 20780.45 - random.randint(100, 100000),
            "Return Percentage 1 yr": -11.75 + random.randint(-10, 10),
            "6 month history": [
                22500.0,
                22100.4,
                21800.6,
                21200.3,
                20950.8,
                20780.45,
            ],
        },
        "TCS": {
            "Name": "Tata Consultancy Services Limited",
            "Price (1 share)": 22390.60 + random.randint(100, 100000),
            "Return Percentage 1 yr": 1.41 - random.randint(-10, 10),
            "6 month history": [
                22100.2,
                22250.5,
                22050.1,
                22400.9,
                22300.4,
                22390.6,
            ],
        },
        "ICICIBANK": {
            "Name": "ICICI Bank Limited",
            "Price (1 share)": 21245.40 - random.randint(100, 100000),
            "Return Percentage 1 yr": 18.20 + random.randint(-10, 10),
            "6 month history": [
                18500.4,
                19200.8,
                19850.2,
                20400.6,
                20900.1,
                21245.4,
            ],
        },
        "INFY": {
            "Name": "Infosys Limited",
            "Price (1 share)": 21255.90 + random.randint(100, 100000),
            "Return Percentage 1 yr": 5.40 - random.randint(-10, 10),
            "6 month history": [
                20200.1,
                20500.4,
                20850.7,
                21000.3,
                21150.9,
                21255.9,
            ],
        },
        "SBIN": {
            "Name": "State Bank of India",
            "Price (1 share)": 21058.00 - random.randint(100, 100000),
            "Return Percentage 1 yr": 31.40 + random.randint(-10, 10),
            "6 month history": [
                16500.5,
                17800.2,
                18900.8,
                19700.4,
                20500.1,
                21058.0,
            ],
        },
        "BHARTIARTL": {
            "Name": "Bharti Airtel Limited",
            "Price (1 share)": 21846.10 + random.randint(100, 100000),
            "Return Percentage 1 yr": 42.10 - random.randint(-10, 10),
            "6 month history": [
                15800.2,
                17200.5,
                18500.1,
                19900.9,
                21000.4,
                21846.1,
            ],
        },
    }

if "bought_stocks" not in st.session_state:
    st.session_state.bought_stocks = {}
if "bankAcc" not in st.session_state:
    st.session_state.bankAcc = {
        "Balance": 100000000.676767 + random.randint(10000, -100000)
    }
if "demat" not in st.session_state:
    st.session_state.dematAcc = {}
if "sold_stocks" not in st.session_state:
    st.session_state.sold_stocks = {}

if "stock_df" not in st.session_state:
    df = pd.DataFrame.from_dict(st.session_state.stock_dict, orient="index")
    df.index.name = "Ticker"
    st.session_state.stock_df = df.reset_index()

if "name" not in st.session_state:
    names = [
        "Liam",
        "Olivia",
        "Noah",
        "Emma",
        "Oliver",
        "Charlotte",
        "James",
        "Amelia",
        "Elijah",
        "Sophia",
        "William",
        "Isabella",
        "Henry",
        "Ava",
        "Lucas",
        "Mia",
        "Benjamin",
        "Evelyn",
        "Theodore",
        "Luna",
        "Mateo",
        "Harper",
        "Levi",
        "Sofia",
        "Sebastian",
        "Scarlett",
        "Daniel",
        "Elizabeth",
        "Jack",
        "Eleanor",
        "Wyatt",
        "Chloe",
        "Alexander",
        "Layla",
        "Owen",
        "Mila",
        "Asher",
        "Alice",
        "Samuel",
        "Hazel",
        "Ethan",
        "Claire",
        "Leo",
        "Ivy",
        "Jackson",
        "Aurora",
        "Mason",
        "Penelope",
        "Ezra",
        "Elena",
    ]
    st.session_state.name = random.choice(names)


def buying_and_stats():
    st.title("View stocks!")
    tl = list(st.session_state.stock_dict.keys())
    pl = list(x["Price (1 share)"] for x in st.session_state.stock_dict.values())

    with st.container(border=True):

        c1, c2 = st.columns([2, 2], border=True)

        with c1:
            st.subheader("Overview of stocks")
            st.divider()
            st.dataframe(st.session_state.stock_df, hide_index=True)
            st.divider()

            f, a = plt.subplots()
            a.barh(tl, pl, color="#00FFFF")
            a.grid(
                True,
                alpha=1.0,
                linewidth=0.5,
                linestyle="-",
                which="both",
                color="#fff",
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
                    key=lambda k: st.session_state.stock_dict[k][
                        "Return Percentage 1 yr"
                    ],
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

            with st.container(border=True):
                buyStock = st.selectbox("Choose a stock to buy", tl)
                noS = st.number_input(
                    "Choose the number of shares you want to buy", 1, None, 1
                )
                s = st.button("Buy")
                st.warning(
                    "Do not click the same stock on the dropdown and the buy button twice or more."
                )

            if s:
                st.session_state.bought_stocks[
                    st.session_state.stock_dict[buyStock]
                ] = {
                    "Name": st.session_state.stock_dict[buyStock]["Name"],
                    "Price (1 share)": st.session_state.stock_dict[buyStock][
                        "Price (1 share)"
                    ],
                    "Return Percentage 1 yr": st.session_state.stock_dict[buyStock][
                        "Return Percentage 1 yr"
                    ],
                    "6 month history": st.session_state.stock_dict[buyStock][
                        "6 month history"
                    ],
                    "No of shares bought": noS,
                }
                st.session_state.demat[buyStock] += (
                    st.session_state.stock_dict[buyStock]["Price (1 share)"]
                    * st.session_state.bought_stocks[buyStock]["No of shares bought"]
                ) * (
                    st.session_state.stock_dict[buyStock]["Return Percentage 1 yr"]
                    / 100
                ) + (
                    st.session_state.stock_dict[buyStock]["Price (1 share)"]
                    * st.session_state.bought_stocks[buyStock]["No of shares bought"]
                )
                st.session_state.bankAcc["Balance"] -= st.session_state.stock_dict[
                    buyStock
                ]["Price (1 share)"]
                * st.session_state.bought_stocks[buyStock]["No of shares bought"]

                an.ani(True, True, False, buyStock)

    with st.container(border=True):
        t1, t2, t3, t4, t5, t6, t7 = st.tabs(tl)

        with t1:
            st.line_chart(
                st.session_state.stock_dict[tl[0]].get("6 month history"),
                color="#3CB371",
            )
        with t2:
            st.line_chart(
                st.session_state.stock_dict[tl[1]].get("6 month history"),
                color="#3CB371",
            )
        with t3:
            st.line_chart(
                st.session_state.stock_dict[tl[2]].get("6 month history"),
                color="#3CB371",
            )
        with t4:
            st.line_chart(
                st.session_state.stock_dict[tl[3]].get("6 month history"),
                color="#3CB371",
            )
        with t5:
            st.line_chart(
                st.session_state.stock_dict[tl[4]].get("6 month history"),
                color="#3CB371",
            )
        with t6:
            st.line_chart(
                st.session_state.stock_dict[tl[5]].get("6 month history"),
                color="#3CB371",
            )
        with t7:
            st.line_chart(
                st.session_state.stock_dict[tl[6]].get("6 month history"),
                color="#3CB371",
            )


def return_calc():
    st.title("Calculate your returns—on point!")
    with st.container(border=True):
        st.subheader("Return calculator")
        st.divider()

        stock_choice = st.selectbox(
            "Choose a stock",
            list(st.session_state.stock_dict.keys()),
        )
        st.divider()

        noShares = st.number_input(
            "Choose the number of shares you want to buy",
            1,
            1000,
            1,
        )
        st.divider()

        st.write(
            f"Return percentage (1 yr) for selected stock: {st.session_state.stock_dict[stock_choice]['Return Percentage 1 yr']}"
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
    if len(st.session_state.bought_stocks) != 0:
        totInv = float(
            sum(
                st.session_state.bought_stocks[a]["Price (1 share)"]
                * st.session_state.bought_stocks[a]["No of shares bought"]
                for a in st.session_state.bought_stocks
            )
        )
        totPL = sum(
            s["Return Percentage 1 yr"]
            / 100
            * s["Price (1 share)"]
            * s["No of shares bought"]
            for s in st.session_state.bought_stocks.values()
        )
        totRet = totPL / totInv * 100
        totPortVal = totInv + totPL

        with st.container("Quick data overview"):
            with st.expander("Total Invested Money"):
                st.metric("Total investment", f"{totInv:.2f} INR")
            with st.expander("Total Portfolio Value"):
                st.metric("Total Portfolio Value", f"{totPortVal:.2f} INR")
            with st.expander("Total P/L (Unrealised)"):
                st.metric("Unrealised P/L", f"{totPL:.2f} INR", f"{totRet:.2f}%")
            with st.expander("Total Realised P/L"):
                st.metric("Total Realised P/L", f"{realisedPL:.2f} INR")
            with st.expander("Bank account balance"):
                st.metric("Bank account", f"{st.session_state.bankAcc["Balance"]} INR")
            with st.expander("Demat account"):
                Tabs = st.tabs(list(st.session_state.bought_stocks.keys()))
                for t in enumerate(Tabs):
                    for i in st.session_state.demat:
                        with t:
                            st.metric(f"Total demat holding for {st.session_state.demat[i]}", )
        c1, c2 = st.columns(2, border=True, gap="large")
        with c1:
            st.subheader("Stock overview")
            st.divider()
            with st.container(border=True):
                taBs = st.tabs(list(st.session_state.bought_stocks.keys()))

                for y, t in enumerate(taBs):
                    with t:
                        bStockDf = pd.Dataframe(
                            list(st.session_state.bought_stocks[y].items())
                        )
                        st.dataframe(bStockDict, hide_index=True)
            with st.container(border=True):
                tAbs = st.tabs(
                    list(
                      st.session_state.bought_stocks.keys()
                    )
                )

                for p, t in enumerate(tAbs):
                    with t:
                        st.line_chart(
                            st.session_state.bought_stocks[p]["6 month history"]
                        )
        with c2:
            st.subheader("Selling market")
            st.divider()
            with st.container(border=True):
                sellStock = st.selectbox(list(st.session_state.bought_stocks.keys()))
                noS = st.number_input(
                    "Choose how many shares you want to sell",
                    1,
                    st.session_state.bought_stocks[sellStock]["No of shares bought"],
                    1,
                )
                sell_conf = st.button("Sell")
                if sell_conf:
                    if (
                        noS
                        == st.session_state.bought_stocks[sellStock][
                            "No of shares bought"
                        ]
                    ):
                        st.session_state.sold_stocks[sellStock] = (
                            st.session_state.bought_stocks[sellStock]
                        )
                        st.session_state.bankAcc["Balance"] += st.session_state.demat[
                            sellStock
                        ]
                        st.session_state.dematAcc[sellStock] = 0.000
                        del st.session_state.bought_stocks[sellStock]
                    else:
                        st.session_state.bought_stocks[sellStock][
                            "No of shares bought"
                        ] -= noS
                        st.session_state.sold_stocks[sellStock] = (
                            st.session_state.bought_stocks[sellStock]
                        )
                        st.session_state.sold_stocks[sellStock][
                            "No of shares bought"
                        ] = noS
                        st.session_state.bankAcc["Balance"] += (
                            st.session_state.bought_stocks[sellStock]["Price"]
                            * noS
                            * (
                                st.session_state.bought_stocks[sellStock][
                                    "Return percentage 1 yr"
                                ]
                                / 100
                            )
                        )
                        st.session_state.demat[sellStock] -= (
                            st.session_state.bought_stocks[sellStock]["Price"] * noS
                        )

    else:
        st.error("No stocks bought!")


def chatbot():
    API_KEY=st.secrets["CHATBOT_API_KEY"]
    with st.container(border=True):
            prompt=st.text_input("Enter a prompt")
            send=st.button("Send")
    with st.container(border=True):
        

