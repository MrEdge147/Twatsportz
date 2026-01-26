import streamlit as st
import random
import pandas as pd

# Page setup
st.set_page_config(page_title="TwatSportz Player Status", page_icon="🏏")

# --- Centered Logo using Streamlit columns ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("twatsportz_logo.png", width=300)

st.title("✏️ TwatSportz Player Status Generator")
st.write("Click a button to assign outcomes to players.")

# --- Player List ---
players = [
    "Ethan Jakarti", "Jerry Cameron", "Archie Burke", "Karl Small", "Daniel Stanton",
    "Jeremy Thiston-Flowers", "Adam Patsalides", "Geoff Wormell", "Billy Patterson",
    "Nicky Cooney", "Tim Crust", "Jimmy Tuckersmith", "Pat James",
    "William Withershaw", "Harvey Last"
]

# --- Outcomes ---
outcomes = [
    "Stay",
    "Out for the season",
    "Leaves",
    "Dead",
    "Works weekends 1 in 4",
    "Getting Married (Miss first 4 games)",
    "Lose 10 Skill Points"
]

# --- Weighting ---
weights = [
    70,  # Stay
    5,   # Out for the season
    5,   # Leaves
    1,   # Dead
    9,   # Works weekends
    5,   # Getting Married
    5    # Lose 10 Skill Points
]

# --- Session State Setup ---
if "remaining_players" not in st.session_state:
    st.session_state.remaining_players = players.copy()

if "single_results" not in st.session_state:
    st.session_state.single_results = []

if "full_results" not in st.session_state:
    st.session_state.full_results = None


# --- Generate ALL Players ---
if st.button("Generate All Player Outcomes"):
    results = []
    for player in players:
        outcome = random.choices(outcomes, weights=weights, k=1)[0]
        results.append({"Player": player, "Outcome": outcome})

    df_full = pd.DataFrame(results)
    df_full.index = df_full.index + 1  # Start at 1
    st.session_state.full_results = df_full


# --- Generate ONE Player ---
if st.button("Generate One Player"):
    if st.session_state.remaining_players:
        player = random.choice(st.session_state.remaining_players)
        outcome = random.choices(outcomes, weights=weights, k=1)[0]

        st.session_state.single_results.append(
            {"Player": player, "Outcome": outcome}
        )

        st.session_state.remaining_players.remove(player)
    else:
        st.warning("All players have already been assigned!")


# --- RESET BUTTON ---
if st.button("Reset"):
    st.session_state.remaining_players = players.copy()
    st.session_state.single_results = []
    st.session_state.full_results = None
    st.success("All data has been reset.")


# --- Display Results ---
if st.session_state.full_results is not None:
    st.subheader("All Player Outcomes")
    st.dataframe(st.session_state.full_results, use_container_width=True, height=700)

if st.session_state.single_results:
    st.subheader("Assigned Players (One-by-One Mode)")
    df_single = pd.DataFrame(st.session_state.single_results)
    df_single.index = df_single.index + 1  # Start at 1
    st.dataframe(df_single, use_container_width=True, height=700)
