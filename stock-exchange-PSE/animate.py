import streamlit as st


class animation:
    def __init__(self, svar, bought: bool, sold: bool, anivar):
        self.svar = svar
        self.anivar = anivar
        self.bought = bought
        self.sold = sold

    def ani(self):
        if self.anivar == True:
            try:
                if self.bought == True and self.sold == False:
                    st.toast(f"You bought {svar}!")
                    st.balloons()
                elif self.bought == False and self.sold == True:
                    st.toast(f"You sold {svar}!")
                    st.balloons()
            except Exception as e:
                raise RunTimeError(f"animate.InputError {e}")
