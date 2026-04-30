import matplotlib.pyplot as plt
import random
import streamlit as st
import pandas as pd
import requests as r
import copy as c
import time as t

st.set_page_config(
    page_title="StockyBankySimulator",
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
        "Bank account": {
            "Balance": 100000000.676767 + random.randint(100, 1000000000000000)
        },
        "No of withdrawals": 0,
        "No of deposits": 0,
        "No of transactions": 0,
        "Withdrawals": [],
        "Deposits": [],
        "Transactions": [],
        "PIN": random.randint(1000, 1000000),
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
        "HINDUNILVR": {
            "Name": "Hindustan Unilever Limited",
            "Price (1 share)": 2450.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 5.20 - random.randint(-10, 10),
            "6 month history": [2300.0, 2350.5, 2400.2, 2420.8, 2440.1, 2450.0],
        },
        "LT": {
            "Name": "Larsen & Toubro Limited",
            "Price (1 share)": 3500.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 45.30 - random.randint(-10, 10),
            "6 month history": [2800.0, 2950.5, 3100.2, 3300.8, 3450.1, 3500.0],
        },
        "BAJFINANCE": {
            "Name": "Bajaj Finance Limited",
            "Price (1 share)": 7100.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 12.80 - random.randint(-10, 10),
            "6 month history": [6800.0, 6950.5, 7050.2, 7000.8, 7050.1, 7100.0],
        },
        "MARUTI": {
            "Name": "Maruti Suzuki India Limited",
            "Price (1 share)": 12500.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 32.15 - random.randint(-10, 10),
            "6 month history": [9500.0, 10200.5, 11000.2, 11800.8, 12200.1, 12500.0],
        },
        "AXISBANK": {
            "Name": "Axis Bank Limited",
            "Price (1 share)": 1150.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 18.90 - random.randint(-10, 10),
            "6 month history": [980.0, 1020.5, 1050.2, 1100.8, 1130.1, 1150.0],
        },
        "KOTAKBANK": {
            "Name": "Kotak Mahindra Bank Limited",
            "Price (1 share)": 1780.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": -3.50 - random.randint(-10, 10),
            "6 month history": [1850.0, 1820.5, 1800.2, 1790.8, 1770.1, 1780.0],
        },
        "ADANIENT": {
            "Name": "Adani Enterprises Limited",
            "Price (1 share)": 3200.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 42.10 - random.randint(-10, 10),
            "6 month history": [2200.0, 2450.5, 2700.2, 2900.8, 3100.1, 3200.0],
        },
        "SUNPHARMA": {
            "Name": "Sun Pharmaceutical Industries Limited",
            "Price (1 share)": 1550.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 55.40 - random.randint(-10, 10),
            "6 month history": [1100.0, 1200.5, 1350.2, 1450.8, 1520.1, 1550.0],
        },
        "TITAN": {
            "Name": "Titan Company Limited",
            "Price (1 share)": 3600.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 28.30 - random.randint(-10, 10),
            "6 month history": [3100.0, 3250.5, 3350.2, 3450.8, 3550.1, 3600.0],
        },
        "ULTRACEMCO": {
            "Name": "UltraTech Cement Limited",
            "Price (1 share)": 9800.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 25.10 - random.randint(-10, 10),
            "6 month history": [8200.0, 8600.5, 9000.2, 9400.8, 9700.1, 9800.0],
        },
        "ASIANPAINT": {
            "Name": "Asian Paints Limited",
            "Price (1 share)": 2850.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": -10.50 - random.randint(-10, 10),
            "6 month history": [3200.0, 3100.5, 3000.2, 2950.8, 2880.1, 2850.0],
        },
        "NTPC": {
            "Name": "NTPC Limited",
            "Price (1 share)": 360.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 88.20 - random.randint(-10, 10),
            "6 month history": [210.0, 245.5, 280.2, 320.8, 345.1, 360.0],
        },
        "M&M": {
            "Name": "Mahindra & Mahindra Limited",
            "Price (1 share)": 2500.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 62.40 - random.randint(-10, 10),
            "6 month history": [1550.0, 1750.5, 1950.2, 2200.8, 2400.1, 2500.0],
        },
        "TATASTEEL": {
            "Name": "Tata Steel Limited",
            "Price (1 share)": 165.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 52.10 - random.randint(-10, 10),
            "6 month history": [115.0, 125.5, 138.2, 150.8, 160.1, 165.0],
        },
        "POWERGRID": {
            "Name": "Power Grid Corporation of India Limited",
            "Price (1 share)": 310.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 75.30 - random.randint(-10, 10),
            "6 month history": [200.0, 225.5, 250.2, 280.8, 300.1, 310.0],
        },
        "ADANIPORTS": {
            "Name": "Adani Ports and Special Economic Zone Limited",
            "Price (1 share)": 1450.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 95.20 - random.randint(-10, 10),
            "6 month history": [800.0, 950.5, 1100.2, 1250.8, 1380.1, 1450.0],
        },
        "WIPRO": {
            "Name": "Wipro Limited",
            "Price (1 share)": 480.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 15.60 - random.randint(-10, 10),
            "6 month history": [410.0, 430.5, 450.2, 490.8, 470.1, 480.0],
        },
        "JSWSTEEL": {
            "Name": "JSW Steel Limited",
            "Price (1 share)": 920.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 28.40 - random.randint(-10, 10),
            "6 month history": [750.0, 780.5, 820.2, 860.8, 900.1, 920.0],
        },
        "ONGC": {
            "Name": "Oil & Natural Gas Corporation Limited",
            "Price (1 share)": 280.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 68.90 - random.randint(-10, 10),
            "6 month history": [180.0, 205.5, 230.2, 255.8, 270.1, 280.0],
        },
        "COALINDIA": {
            "Name": "Coal India Limited",
            "Price (1 share)": 475.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 110.20 - random.randint(-10, 10),
            "6 month history": [250.0, 310.5, 380.2, 420.8, 460.1, 475.0],
        },
        "Tatamotors": {
            "Name": "Tata Motors Limited",
            "Price (1 share)": 980.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 115.40 - random.randint(-10, 10),
            "6 month history": [520.0, 640.5, 780.2, 890.8, 950.1, 980.0],
        },
        "HCLTECH": {
            "Name": "HCL Technologies Limited",
            "Price (1 share)": 1450.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 32.10 - random.randint(-10, 10),
            "6 month history": [1150.0, 1250.5, 1320.2, 1480.8, 1410.1, 1450.0],
        },
        "BAJAJ-AUTO": {
            "Name": "Bajaj Auto Limited",
            "Price (1 share)": 9200.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 98.50 - random.randint(-10, 10),
            "6 month history": [5100.0, 6200.5, 7500.2, 8400.8, 8900.1, 9200.0],
        },
        "NESTLEIND": {
            "Name": "Nestle India Limited",
            "Price (1 share)": 2550.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 18.20 - random.randint(-10, 10),
            "6 month history": [2200.0, 2300.5, 2450.2, 2400.8, 2500.1, 2550.0],
        },
        "GRASIM": {
            "Name": "Grasim Industries Limited",
            "Price (1 share)": 2400.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 35.10 - random.randint(-10, 10),
            "6 month history": [1850.0, 1980.5, 2100.2, 2250.8, 2350.1, 2400.0],
        },
        "SBILIFE": {
            "Name": "SBI Life Insurance Company Limited",
            "Price (1 share)": 1450.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 22.40 - random.randint(-10, 10),
            "6 month history": [1200.0, 1280.5, 1350.2, 1410.8, 1430.1, 1450.0],
        },
        "TECHM": {
            "Name": "Tech Mahindra Limited",
            "Price (1 share)": 1350.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 25.10 - random.randint(-10, 10),
            "6 month history": [1100.0, 1180.5, 1250.2, 1320.8, 1340.1, 1350.0],
        },
        "HINDALCO": {
            "Name": "Hindalco Industries Limited",
            "Price (1 share)": 680.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 62.40 - random.randint(-10, 10),
            "6 month history": [450.0, 520.5, 580.2, 630.8, 660.1, 680.0],
        },
        "BAJAJFINSV": {
            "Name": "Bajaj Finserv Limited",
            "Price (1 share)": 1600.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 15.20 - random.randint(-10, 10),
            "6 month history": [1450.0, 1520.5, 1580.2, 1620.8, 1590.1, 1600.0],
        },
        "CIPLA": {
            "Name": "Cipla Limited",
            "Price (1 share)": 1480.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 42.10 - random.randint(-10, 10),
            "6 month history": [1050.0, 1180.5, 1300.2, 1420.8, 1460.1, 1480.0],
        },
        "BRITANNIA": {
            "Name": "Britannia Industries Limited",
            "Price (1 share)": 5200.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 12.50 - random.randint(-10, 10),
            "6 month history": [4600.0, 4800.5, 5000.2, 5100.8, 5150.1, 5200.0],
        },
        "EICHERMOT": {
            "Name": "Eicher Motors Limited",
            "Price (1 share)": 4600.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 35.80 - random.randint(-10, 10),
            "6 month history": [3400.0, 3700.5, 4000.2, 4300.8, 4500.1, 4600.0],
        },
        "ADANIPOWER": {
            "Name": "Adani Power Limited",
            "Price (1 share)": 750.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 210.40 - random.randint(-10, 10),
            "6 month history": [250.0, 380.5, 520.2, 640.8, 710.1, 750.0],
        },
        "TATAELXSI": {
            "Name": "Tata Elxsi Limited",
            "Price (1 share)": 7800.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 5.20 - random.randint(-10, 10),
            "6 month history": [7400.0, 7600.5, 7700.2, 7900.8, 7750.1, 7800.0],
        },
        "INDUSINDBK": {
            "Name": "IndusInd Bank Limited",
            "Price (1 share)": 1500.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 22.40 - random.randint(-10, 10),
            "6 month history": [1300.0, 1380.5, 1420.2, 1480.8, 1470.1, 1500.0],
        },
        "DIVISLAB": {
            "Name": "Divi's Laboratories Limited",
            "Price (1 share)": 3950.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 18.20 - random.randint(-10, 10),
            "6 month history": [3400.0, 3550.5, 3700.2, 3850.8, 3900.1, 3950.0],
        },
        "DRREDDY": {
            "Name": "Dr. Reddy's Laboratories Limited",
            "Price (1 share)": 6200.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 32.40 - random.randint(-10, 10),
            "6 month history": [4800.0, 5200.5, 5600.2, 5900.8, 6100.1, 6200.0],
        },
        "APOLLOHOSP": {
            "Name": "Apollo Hospitals Enterprise Limited",
            "Price (1 share)": 6300.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 45.10 - random.randint(-10, 10),
            "6 month history": [4500.0, 4900.5, 5400.2, 5900.8, 6150.1, 6300.0],
        },
        "HEROMOTOCO": {
            "Name": "Hero MotoCorp Limited",
            "Price (1 share)": 5100.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 82.40 - random.randint(-10, 10),
            "6 month history": [2800.0, 3400.5, 4100.2, 4600.8, 4950.1, 5100.0],
        },
        "BPCL": {
            "Name": "Bharat Petroleum Corporation Limited",
            "Price (1 share)": 620.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 78.50 - random.randint(-10, 10),
            "6 month history": [350.0, 420.5, 490.2, 560.8, 600.1, 620.0],
        },
        "ZOMATO": {
            "Name": "Zomato Limited",
            "Price (1 share)": 190.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 185.20 - random.randint(-10, 10),
            "6 month history": [70.0, 95.5, 125.2, 155.8, 175.1, 190.0],
        },
        "PAYTM": {
            "Name": "One 97 Communications Limited",
            "Price (1 share)": 400.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": -45.20 - random.randint(-10, 10),
            "6 month history": [850.0, 720.5, 600.2, 420.8, 380.1, 400.0],
        },
        "IRCTC": {
            "Name": "Indian Railway Catering and Tourism Corporation Limited",
            "Price (1 share)": 1000.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 65.40 - random.randint(-10, 10),
            "6 month history": [650.0, 720.5, 840.2, 920.8, 970.1, 1000.0],
        },
        "HAL": {
            "Name": "Hindustan Aeronautics Limited",
            "Price (1 share)": 4500.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 165.20 - random.randint(-10, 10),
            "6 month history": [1800.0, 2400.5, 3100.2, 3800.8, 4300.1, 4500.0],
        },
        "BEL": {
            "Name": "Bharat Electronics Limited",
            "Price (1 share)": 280.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 125.40 - random.randint(-10, 10),
            "6 month history": [130.0, 165.5, 205.2, 245.8, 265.1, 280.0],
        },
        "TATACOMM": {
            "Name": "Tata Communications Limited",
            "Price (1 share)": 1850.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 32.40 - random.randint(-10, 10),
            "6 month history": [1550.0, 1620.5, 1700.2, 1780.8, 1820.1, 1850.0],
        },
        "JIOFIN": {
            "Name": "Jio Financial Services Limited",
            "Price (1 share)": 350.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 45.80 - random.randint(-10, 10),
            "6 month history": [240.0, 265.5, 290.2, 320.8, 340.1, 350.0],
        },
        "DLF": {
            "Name": "DLF Limited",
            "Price (1 share)": 880.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 110.20 - random.randint(-10, 10),
            "6 month history": [450.0, 560.5, 680.2, 790.8, 850.1, 880.0],
        },
        "GAIL": {
            "Name": "GAIL (India) Limited",
            "Price (1 share)": 210.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 95.40 - random.randint(-10, 10),
            "6 month history": [110.0, 135.5, 158.2, 182.8, 198.1, 210.0],
        },
        "PIDILITIND": {
            "Name": "Pidilite Industries Limited",
            "Price (1 share)": 2950.00 + random.randint(100, 100000),
            "Return Percentage 1 yr": 22.10 - random.randint(-10, 10),
            "6 month history": [2450.0, 2580.5, 2700.2, 2820.8, 2900.1, 2950.0],
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
    for i, j in zip(st.tabs(tickerList), tickerList):
        with i:
            st.write(j)
            st.divider()
            st.line_chart(
                pd.DataFrame(st.session_state.availableStocks[j]["6 month history"]),
                color="#17807e",
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
    ph = st.empty()
    with ph:
        with st.container(border=True):
            st.write(f"Your PIN is {st.session_state.userDict["PIN"]}")
            t.sleep(5)
        ph.empty()
    st.caption(
        "This game is purely made for educational purposes. No misuse cases are attributed to the developer."
    )


def bankManagement():
    names = [
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

    class withDraw:
        def __init__(self, name: str, amount: float, withdrawalNo: int):
            self.name = name
            self.amount = amount
            self.withdrawalNo = withdrawalNo

        def dict(self):
            return {
                "Name": self.name,
                "Amount": self.amount,
                "Withdrawal number": self.withdrawalNo,
            }

        def celebrate(self):
            st.success("Withdrawal successful!")

    class deposit:
        def __init__(self, name: str, amount: float, depositNo: int):
            self.name = name
            self.amount = amount
            self.withdrawalNo = depositNo

        def dict(self):
            return {
                "Name": self.name,
                "Amount": self.amount,
                "Deposit number": self.depositNo,
            }

        def celebrate(self):
            st.success("Deposit successful!")

    class transaction:
        def __init__(self, name: str, amount: float, transactionNo: int, receiver: str):
            self.name = name
            self.amount = amount
            self.withdrawalNo = transactionNo
            self.receiver = receiver

        def dict(self):
            return {
                "Name": self.name,
                "Amount": self.amount,
                "Transaction number": self.transactionNo,
                "Receiver": self.receiver,
            }

        def celebrate(self):
            st.success("Transaction successful!")

    c1, c2, c3 = st.columns(3, border=True)
    with c1:
        st.subheader("Withdrawals here!")
        st.divider()
        with st.container(border=True):
            withdrawalName = st.text_input("Enter the name of your withdrawal")
            pin = int(st.text_input("Enter your PIN", type="password"))
            amountWithdrawn = st.slider(
                label="How much do you want to withdraw",
                min=1.00,
                max=st.session_state.userDict["Bank account balance"],
                step=1,
            )
        if withdrawalName and pin and amountWithdrawn:
            if pin == st.session_state.userDict["PIN"]:
                withdrawal = withDraw(
                    withdrawalName, amountWithdrawn, random.randint(1000, 1000000000)
                )
                st.session_state.userDict["Withdrawals"].append(withdrawal.dict())
                st.session_state.userDict["No of withdrawals"] += 1
                st.session_state.userDict["Bank account balance"] -= amountWithdrawn
                withdrawal.celebrate()
            else:
                st.error("Enter a new PIN. The submitted PIN is wrong.")
    with c2:
        st.subheader("Transactions here!")
        st.divider()
        with st.container(border=True):
            transactionName = st.text_input("Enter the name of your withdrawal")
            pinTra = int(st.text_input("Enter your PIN", type="password"))
            amountSent = st.slider(
                label="How much do you want to send",
                min=1.00,
                max=st.session_state.userDict["Bank account balance"],
                step=1,
            )
            receiver = st.selectbox("Who do you want to send the money to?", names)
            if transactionName and pinTra and amountSent:
                if pin == st.session_state.userDict["PIN"]:
                    withdrawal = transaction(
                        withdrawalName,
                        amountWithdrawn,
                        random.randint(1000, 1000000000),
                        receiver,
                    )
                    st.session_state.userDict["Transactions"].append(transaction.dict())
                    st.session_state.userDict["Bank account balance"] -= amountSent
                    st.session_state.userDict["No of transactions"] += 1
                    withdrawal.celebrate()
                else:
                    st.error("Enter a new PIN. The submitted PIN is wrong.")
    with c3:
        st.subheader("Deposits here!")
        st.divider()
        with st.container(border=True):
            DepositName = st.text_input("Enter the name of your deposit")
            pin = int(st.text_input("Enter your PIN", type="password"))
            amountDeposited = st.slider(
                label="How much do you want to deposit",
                min=1.00,
                max=st.session_state.userDict["Bank account balance"],
                step=1,
            )
        if withdrawalName and pin and amountWithdrawn:
            if pin == st.session_state.userDict["PIN"]:
                dep = deposit(
                    DepositName, amountDeposited, random.randint(1000, 1000000000)
                )
                st.session_state.userDict["Deposits"].append(dep.dict())
                st.session_state.userDict["Bank account balance"] += amountDeposited
                st.session_state.userDict["No of deposits"] += 1
                dep.celebrate()
            else:
                st.error("Enter a new PIN. The submitted PIN is wrong.")


with st.sidebar:
    choiceList = [
        "View stock stats and buy some stocks",
        "Calculate the return percentage of stocks",
        "View your portfolio and sell stocks",
        "Use the chatbot",
        "Read the instruction manual",
        "Manage your bank account",
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
if a == choiceList[5]:
    pass
