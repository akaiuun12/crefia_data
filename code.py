import numpy as np 
import pandas as pd

import streamlit as st

st.title("Hello, Streamlit!")
st.header("This is a header", divider=True)
st.subheader("This is a subheader", divider=True)
st.text("This is a text element.")
st.markdown("This is a **markdown** element.")

x = st.slider("Select a value", 0, 100, 50)
st.write(f"You selected :red[{x}]")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
st.line_chart(chart_data)
