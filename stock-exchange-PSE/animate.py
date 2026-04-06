import streamlit as st


def ani(anivar: bool, bought: bool, sold: bool, svar):
    if anivar == True:
        try:
            if bought == True and sold == False:
                st.toast(f"You bought {svar}!")
                st.balloons()
            elif bought == False and sold == True:
                st.toast(f"You sold {svar}!")
                st.balloons()
        except Exception as e:
            raise RuntimeError(f"animate.InputError {e}")


def aniCustom(anivar: bool, aniString: str, negativeBank: bool):
    if anivar == True:
        try:
            st.toast(f"{aniString}!")
            if negativeBank == False:
                st.balloons()
        except Exception as e:
            raise RuntimeError(f"animate.InputError {e}")
