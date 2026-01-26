import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="TwatSportz Player Status", page_icon="🏏")

# --- Centered Logo using Streamlit columns ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("twatsportz_logo.png", width=300)

st.title("✏️ TwatSportz Player Status Generator")
st.write("Click the button to assign a random (weighted) outcome to each player.")

players = [
    "Ethan Jakarti", "Jerry Cameron", "Archie Burke", "Karl Small", "Daniel Stanton",
    "Jeremy Thiston-Flowers", "Adam Patsalides", "Geoff Wormell", "Billy Patterson",
    "Nicky Cooney", "Tim Crust", "Jimmy Tuckersmith", "Pat James",
    "William Withershaw", "Harvey Last"
]

outcomes = [
    "Stay",
    "Out for the season",
    "Leaves",
    "Dead",
    "Works weekends 1 in 4",
    "Getting Married (Miss first 4 games)",
    "Lose 10 Skill Points"
]

weights = [
    70,
    5,
    5,
    1,
    9,
    5,
    5
]

if st.button("Generate Player Outcomes"):
    results = []

    for player in players:
        outcome = random.choices(outcomes, weights=weights, k=1)[0]
        results.append({"Player": player, "Outcome": outcome})

    df = pd.DataFrame(results)
    st.subheader("Results")
    st.dataframe(df, use_container_width=True)
