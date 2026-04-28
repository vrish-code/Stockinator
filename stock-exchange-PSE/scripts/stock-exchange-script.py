import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import requests as r
import copy as c

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


instructions = [
    "Do not click on the same stock in buy or sell twice.",
    "Do not misuse the chatbot.",
    "Use this to learn the basics of trading.",
    "All values are simulated, not real. No changes happen to a real bank account.",
    "Navigate between pages using the sidebar's dropdown menu",
    "Read the graphs and data carefully and buy or sell your stocks.",
    "Use the dropdowns for selecting stocks.",
    "Use the expanders for viewing your portfolio data at a glance.",
]
if "gender" not in st.session_state:
    st.session_state.gender = random.choice(["Boy", "Girl"])
if "userDict" not in st.session_state:
    st.session_state.userDict = {
        "Bought stocks": {},
        "Sold stocks": {},
        "Bank account": {"Balance": 100000000.676767 + random.randint(-10000, 100000)},
        "Demat": {},
        "Name": (
            random.choice(
                [
                    "Liam",
                    "Noah",
                    "Oliver",
                    "James",
                    "Elijah",
                    "William",
                    "Henry",
                    "Lucas",
                    "Benjamin",
                    "Theodore",
                    "Mateo",
                    "Levi",
                    "Sebastian",
                    "Daniel",
                    "Jack",
                    "Wyatt",
                    "Alexander",
                    "Owen",
                    "Asher",
                    "Samuel",
                    "Ethan",
                    "Leo",
                    "Jackson",
                    "Mason",
                    "Ezra",
                ]
            )
            if st.session_state.gender == "Boy"
            else random.choice(
                [
                    "Olivia",
                    "Emma",
                    "Charlotte",
                    "Amelia",
                    "Sophia",
                    "Isabella",
                    "Ava",
                    "Mia",
                    "Evelyn",
                    "Luna",
                    "Harper",
                    "Sofia",
                    "Scarlett",
                    "Elizabeth",
                    "Eleanor",
                    "Chloe",
                    "Layla",
                    "Mila",
                    "Alice",
                    "Hazel",
                    "Claire",
                    "Ivy",
                    "Aurora",
                    "Penelope",
                    "Elena",
                ]
            )
        ),
    }

if "availableStocks" not in st.session_state:
    st.session_state.availableStocks = {
        "RELIANCE": {
            "Name": "Reliance Industries Limited",
            "Price (1 share)": 2985.40 + random.randint(100, 100000),
            "Return Percentage 1 yr": 18.50 - random.randint(-10, 10),
            "6 month history": [2450.5, 2580.2, 2710.8, 2840.4, 2920.1, 2985.4],
        },
        "HDFCBANK": {
            "Name": "HDFC Bank Limited",
            "Price (1 share)": 1642.15 - random.randint(100, 100000),
            "Return Percentage 1 yr": 4.25 + random.randint(-10, 10),
            "6 month history": [1520.0, 1480.4, 1550.6, 1610.3, 1630.8, 1642.15],
        },
        "TCS": {
            "Name": "Tata Consultancy Services Limited",
            "Price (1 share)": 3950.60 + random.randint(100, 100000),
            "Return Percentage 1 yr": 15.41 - random.randint(-10, 10),
            "6 month history": [3410.2, 3550.5, 3680.1, 3820.9, 3910.4, 3950.6],
        },
        "ICICIBANK": {
            "Name": "ICICI Bank Limited",
            "Price (1 share)": 1125.40 - random.randint(100, 100000),
            "Return Percentage 1 yr": 22.20 + random.randint(-10, 10),
            "6 month history": [950.4, 990.8, 1040.2, 1080.6, 1110.1, 1125.4],
        },
        "INFY": {
            "Name": "Infosys Limited",
            "Price (1 share)": 1545.90 + random.randint(100, 100000),
            "Return Percentage 1 yr": 12.40 - random.randint(-10, 10),
            "6 month history": [1380.1, 1420.4, 1460.7, 1490.3, 1520.9, 1545.9],
        },
        "BHARTIARTL": {
            "Name": "Bharti Airtel Limited",
            "Price (1 share)": 1420.10 + random.randint(100, 100000),
            "Return Percentage 1 yr": 65.10 - random.randint(-10, 10),
            "6 month history": [880.2, 950.5, 1100.1, 1250.9, 1380.4, 1420.1],
        },
        "SBIN": {
            "Name": "State Bank of India",
            "Price (1 share)": 785.00 - random.randint(100, 100000),
            "Return Percentage 1 yr": 35.40 + random.randint(-10, 10),
            "6 month history": [580.5, 620.2, 680.8, 720.4, 760.1, 785.0],
        },
        "LICI": {
            "Name": "Life Insurance Corporation of India",
            "Price (1 share)": 1015.45 + random.randint(100, 100000),
            "Return Percentage 1 yr": 72.86 - random.randint(-10, 10),
            "6 month history": [610.1, 680.4, 820.1, 940.5, 990.3, 1015.45],
        },
        "ITC": {
            "Name": "ITC Limited",
            "Price (1 share)": 435.65 + random.randint(100, 100000),
            "Return Percentage 1 yr": 5.77 - random.randint(-10, 10),
            "6 month history": [410.8, 425.4, 440.1, 455.6, 442.2, 435.65],
        },
        "LTIM": {
            "Name": "LTIMindtree Limited",
            "Price (1 share)": 4850.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": -2.30 - random.randint(-10, 10),
            "6 month history": [5200.4, 5100.1, 4950.5, 4880.2, 4820.4, 4850.0],
        },
    }

if "stock_df" not in st.session_state:
    st.session_state.stock_df = (
        pd.DataFrame.from_dict(st.session_state.availableStocks, orient="index")
        .reset_index()
        .rename(columns={"index": "Ticker"})
    )


def buyingAndStats():
    st.title("View available stocks!")
    st.divider()
    st.subheader(f"Welcome, {st.session_state.userDict["Name"]}! ")
    tl = list(st.session_state.availableStocks.keys())
    pl = list(x["Price (1 share)"] for x in st.session_state.availableStocks.values())

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
            a.set_xlim(0, 100000)
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
                for x in st.session_state.availableStocks.values()
            ]
            retPerSort = list(sorted(retpr, reverse=True))

            g, h = plt.subplots()
            h.barh(
                sorted(
                    list(st.session_state.availableStocks.keys()),
                    key=lambda k: st.session_state.availableStocks[k][
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
                st.session_state.userDict["Bought stocks"][buyStock] = c.deepcopy(
                    st.session_state.availableStocks[buyStock]
                )
                st.session_state.userDict["Bought stocks"][buyStock][
                    "No of shares bought"
                ] = noS
                st.session_state.userDict["Demat"][buyStock] = 0
                st.session_state.userDict["Demat"][buyStock] += (
                    st.session_state.userDict["Bought stocks"][buyStock][
                        "Price (1 share)"
                    ]
                    * noS
                ) * (
                    st.session_state.userDict["Bought stocks"][buyStock][
                        "Return Percentage 1 yr"
                    ]
                    / 100
                ) + (
                    st.session_state.userDict["Bought stocks"][buyStock][
                        "Price (1 share)"
                    ]
                    * noS
                )
                st.session_state.userDict["Bank account"]["Balance"] -= (
                    st.session_state.availableStocks[buyStock]["Price (1 share)"]
                    * st.session_state.userDict["Bought stocks"][buyStock][
                        "No of shares bought"
                    ]
                )
                st.success(f"You bought {buyStock}!")
                st.divider()
    st.divider()
    tickerList = list(st.session_state.availableStocks.keys())
    with st.container(border=True):
        tabs = st.tabs(tickerList)
        for i in tabs:
            for j in range(len(tickerList)):
                for k in st.session_state.availableStocks:
                    with i:
                        st.line_chart(
                            st.session_state.availableStocks[k]["6 month history"],
                            x=f"{k}",
                            y="Price Trend (6 months)",
                            color="#176d74",
                        )


def returnCalc():
    st.title("Calculate your returns—on point! Decide wisely.")
    with st.container(border=True):
        st.subheader("Return calculator")
        st.divider()

        stock_choice = st.selectbox(
            "Choose a stock",
            list(st.session_state.availableStocks.keys()),
        )
        st.divider()

        noShares = st.number_input(
            "Choose the number of shares you want to buy",
            1,
            None,
            1,
        )
        st.divider()

        st.write(
            f"Return percentage (1 yr) for selected stock: {st.session_state.availableStocks[stock_choice]['Return Percentage 1 yr']}"
        )
        st.divider()

        ret_output = (
            st.session_state.availableStocks[stock_choice]["Price (1 share)"] * noShares
        ) * (
            st.session_state.availableStocks[stock_choice]["Return Percentage 1 yr"]
            / 100
        )

        st.metric("Return output", f"₹{ret_output}")
        st.divider()


def chatbot():
    with st.container(border=True):
        prompt = st.chat_input("Enter a prompt")
    realPrompt = f"""Stocks available:{st.session_state.availableStocks}, 
    Bought stocks: {st.session_state.userDict["Bought stocks"]}, 
    Sold stocks: {st.session_state.userDict["Sold stocks"]}, 
    Bank account: {st.session_state.userDict["Bank account"]}, 
    Demat account: {st.session_state.userDict["Demat"]}, {prompt}, do not provide any inappropriate misinformation. The data is just for
    a simulator. Don't think the user is actually trading stocks."""
    with st.container(border=True):
        with st.chat_message("Stockinator.ai", avatar="🤖"):
            st.write(f"How can I help you {st.session_state.userDict["Name"]}?")
        if prompt:
            with st.chat_message(st.session_state.userDict["Name"], avatar="👤"):
                st.write(prompt)
            with st.spinner("Stockinator.ai is thinking..."):
                resp = r.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {st.secrets["apiKeyChatbot"]}",
                        "Content-Type": "application/json",
                    },
                    json={
                        "model": "openrouter/free",
                        "messages": [{"role": "user", "content": realPrompt}],
                    },
                )
                if resp.status_code == 200:
                    with st.chat_message("Stockinator.ai", avatar="🤖"):
                        st.write(f"{resp.json()['choices'][0]['message']['content']}")


def portfolioAndSelling():

    st.header("Portfolio")
    st.divider()
    st.subheader(f"Welcome, {st.session_state.userDict["Name"]}!")
    if len(st.session_state.userDict["Bought stocks"]) != 0:
        totInv = float(
            sum(
                st.session_state.userDict["Bought stocks"][a]["Price (1 share)"]
                * st.session_state.userDict["Bought stocks"][a]["No of shares bought"]
                for a in st.session_state.userDict["Bought stocks"]
            )
        )
        totPL = sum(
            s["Return Percentage 1 yr"]
            / 100
            * s["Price (1 share)"]
            * s["No of shares bought"]
            for s in st.session_state.userDict["Bought stocks"].values()
        )
        totRet = totPL / totInv * 100
        totPortVal = totInv + totPL

        with st.container():
            st.subheader("Quick data overview")
            with st.expander("Total Invested Money"):
                st.metric("Total investment", f"{totInv:.2f} INR")
            with st.expander("Total Portfolio Value"):
                st.metric("Total Portfolio Value", f"{totPortVal:.2f} INR")
            with st.expander("Total P/L (Unrealised)"):
                st.metric("Unrealised P/L", f"{totPL:.2f} INR", f"{totRet:.2f}%")

            with st.expander("Bank account balance"):
                st.metric(
                    f"Bank account balance for {st.session_state.userDict["Name"]}",
                    f"{st.session_state.userDict["Bank account"]["Balance"]} INR",
                )
            with st.expander("Demat"):
                dTL = list(st.session_state.userDict["Demat"].keys())
                for i in range(len(dTL)):
                    st.metric(
                        f"Demat holding for {dTL[i]}",
                        f"{st.session_state.userDict["Demat"][dTL[i]]:.2f} INR",
                    )
                    st.divider()

        t1, t2 = st.tabs(["Stock overview", "Selling"])
        with t1:
            with st.container(border=True):
                st.subheader("Stock overview")
                st.divider()
                t3, t4 = st.tabs(
                    [
                        "Overview of all bought stocks",
                        "6 month histories of all bought stocks",
                    ]
                )
                with t3:
                    with st.container(border=True):
                        sList = list(st.session_state.userDict["Bought stocks"].keys())
                        for i in st.session_state.userDict["Bought stocks"]:
                            with st.container(border=True):
                                st.subheader(sList[sList.index(i)])
                                bSDf = pd.DataFrame(
                                    list(
                                        st.session_state.userDict["Bought stocks"][
                                            i
                                        ].items(),
                                    ),
                                    columns=["Categories", "Details"],
                                )
                                st.dataframe(bSDf, hide_index=True)
                with t4:
                    with st.container(border=True):
                        for i in st.session_state.userDict["Bought stocks"]:
                            with st.container(border=True):
                                st.caption(
                                    f"6 month history for {st.session_state.userDict["Bought stocks"][i][
                                    "6 month history"
                                ]}"
                                )
                                st.line_chart(
                                    st.session_state.userDict["Bought stocks"][i][
                                        "6 month history"
                                    ]
                                )
        with t2:
            with st.container(border=True):
                st.subheader("Selling")
            with st.container(border=True):
                sellStock = st.selectbox(
                    "Choose a stock to sell",
                    list(st.session_state.userDict["Bought stocks"].keys()),
                )
                noS = st.number_input(
                    "How many shares do you want to sell?",
                    1,
                    st.session_state.userDict["Bought stocks"][sellStock][
                        "No of shares bought"
                    ],
                )
                sellConf = st.button("Sell")
                if sellConf:
                    if (
                        noS
                        == st.session_state.userDict["Bought stocks"][sellStock][
                            "No of shares bought"
                        ]
                    ):
                        st.session_state.userDict["Sold stocks"][sellStock] = (
                            st.session_state.userDict["Bought stocks"][sellStock]
                        )
                        del st.session_state.userDict["Bought stocks"][sellStock]
                        st.session_state.userDict["Bank account"][
                            "Balance"
                        ] += st.session_state.userDict["Demat"][sellStock]

                        st.rerun()
                    elif (
                        noS
                        != st.session_state.userDict["Bought stocks"][sellStock][
                            "No of shares bought"
                        ]
                    ):
                        st.session_state.userDict["Bought stocks"][sellStock][
                            "No of shares bought"
                        ] -= noS
                        st.session_state.userDict["Sold stocks"][sellStock] = (
                            st.session_state.userDict["Bought stocks"][sellStock]
                        )
                        st.session_state.userDict["Sold stocks"][sellStock][
                            "No of shares bought"
                        ] = noS
                        st.session_state.userDict["Bank account"]["Balance"] += (
                            st.session_state.userDict["Bought stocks"][sellStock][
                                "Price (1 share)"
                            ]
                            * noS
                        ) * (
                            st.session_state.userDict["Bought stocks"][sellStock][
                                "Return Percentage 1 yr"
                            ]
                            / 100
                        ) + (
                            st.session_state.userDict["Bought stocks"][sellStock][
                                "Price (1 share)"
                            ]
                            * noS
                        )
                        st.session_state.userDict["Demat"][sellStock] = 0
                        st.session_state.userDict["Demat"][sellStock] = (
                            (
                                st.session_state.userDict["Bought stocks"][sellStock][
                                    "Price (1 share)"
                                ]
                                * noS
                            )
                            * (
                                st.session_state.userDict["Bought stocks"][sellStock][
                                    "Return Percentage 1 yr"
                                ]
                                / 100
                            )
                            + (
                                st.session_state.userDict["Bought stocks"][sellStock][
                                    "Price (1 share)"
                                ]
                                * noS
                            )
                            - noS
                        )

                        st.rerun()
            st.divider()

    else:
        st.error("No stocks bought!")


def inStructions():
    for i in range(len(instructions)):
        st.warning(instructions[i])
        st.divider()
    st.success("Happy trading!")
    st.divider()
    st.caption(
        "This game is purely made for educational purposes. No misuse cases are attributed to the developer."
    )


with st.sidebar:
    choiceList = [
        "View stock stats and buy some stocks",
        "Calculate the return percentage of stocks",
        "View your portfolio and sell stocks",
        "Use the chatbot",
        "Read the instruction manual",
    ]
    st.sidebar.title("Navigate between pages using the sidebar's dropdown menu")
    a = st.selectbox(
        "Choice",
        choiceList,
    )
if a == choiceList[0]:
    buyingAndStats()
if a == choiceList[2]:
    portfolioAndSelling()
if a == choiceList[3]:
    chatbot()
if a == choiceList[1]:
    returnCalc()
if a == choiceList[4]:
    inStructions()
