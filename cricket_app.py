import streamlit as st
import random
import pandas as pd

# Page setup
st.set_page_config(page_title="Chiddingly Player Status", page_icon="🏏")

# --- Global CSS: Zoom page + tighten spacing + add card styling ---
page_css = """
<style>
html {
    zoom: 1.2;
}

.block-container {
    max-width: 1100px;
    margin-left: auto;
    margin-right: auto;
}

/* Card-style panels for left and right columns */
.card {
    background-color: #222;
    padding: 12px 15px;
    border-radius: 8px;
    border: 1px solid #444;
}

/* Player names = white */
.player-name {
    margin: 0px;
    padding: 0px;
    line-height: 1.15;
    font-size: 15px;
    color: white;
}

/* Outcome names = black */
.outcome-name {
    margin: 0px;
    padding: 0px;
    line-height: 1.15;
    font-size: 15px;
    color: black;
}

/* Colour-coded outcomes on the right */
.outcome-Stay { background-color: #c8f7c5; padding: 2px 4px; border-radius: 4px; }
.outcome-Out { background-color: #f7d4c5; padding: 2px 4px; border-radius: 4px; }
.outcome-Leaves { background-color: #fce5cd; padding: 2px 4px; border-radius: 4px; }
.outcome-Dead { background-color: #ffb3b3; padding: 2px 4px; border-radius: 4px; }
.outcome-Weekends { background-color: #fff2cc; padding: 2px 4px; border-radius: 4px; }
.outcome-Married { background-color: #d9d2e9; padding: 2px 4px; border-radius: 4px; }
.outcome-Skill { background-color: #cfe2f3; padding: 2px 4px; border-radius: 4px; }

/* Add spacing under buttons */
.stButton > button {
    margin-top: 10px;
    margin-bottom: 10px;
}
</style>
"""
st.markdown(page_css, unsafe_allow_html=True)

# --- Player List ---
players = [
    "Ethan Jakarti", "Jerry Cameron", "Archie Burke", "Karl Small", "Daniel Stanton",
    "Jeremy Thiston-Flowers", "Adam Patsalides", "Geoff Wormell", "Billy Patterson",
    "Nicky Cooney", "Tim Crust", "Jimmy Tuckersmith", "Pat James",
    "William Withershaw", "Harvey Last"
]

# --- Outcomes List ---
outcomes = [
    "Stay",
    "Out for the season",
    "Leaves",
    "Dead",
    "Works weekends 1 in 4",
    "Getting Married (Miss first 4 games)",
    "Lose 10 Skill Points"
]

# --- Dynamic weights stored in session state ---
if "current_weights" not in st.session_state:
    st.session_state.current_weights = {
        "Stay": 70,
        "Out for the season": 5,
        "Leaves": 5,
        "Dead": 1,
        "Works weekends 1 in 4": 9,
        "Getting Married (Miss first 4 games)": 5,
        "Lose 10 Skill Points": 5
    }

# --- Three-column layout: LEFT = players, MIDDLE = app, RIGHT = outcomes ---
left_col, mid_col, right_col = st.columns([0.8, 3.0, 0.8])

# LEFT COLUMN — static player list inside a card
with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Players</h3>", unsafe_allow_html=True)
    for p in players:
        st.markdown(f"<p class='player-name'>{p}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN — static outcomes list inside a card
with right_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Outcomes</h3>", unsafe_allow_html=True)

    st.markdown("<p class='outcome-name outcome-Stay'>Stay</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Out'>Out for the season</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Leaves'>Leaves</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Dead'>Dead</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Weekends'>Works weekends 1 in 4</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Married'>Getting Married (Miss first 4 games)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Skill'>Lose 10 Skill Points</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# MIDDLE COLUMN — full app content
with mid_col:

    # --- Centered Logo + Title ---
    header_left, header_mid, header_right = st.columns([1, 2, 1])

    with header_mid:
        st.image("twatsportz_logo.png", width=400)
        st.markdown(
            """
            <h1 style='text-align:center; line-height:1.2; margin-bottom: 20px;'>
                Chiddingly<br>Player Status Generator
            </h1>
            """,
            unsafe_allow_html=True
        )

    # --- Probability Meter ---
    st.markdown("<h3 style='text-align:center; margin-top:20px;'>Outcome Probabilities</h3>", unsafe_allow_html=True)

    total_weight = sum(st.session_state.current_weights[o] for o in outcomes)

    for o in outcomes:
        prob = st.session_state.current_weights[o] / total_weight

        st.markdown(
            f"<div style='font-size:15px; text-align:left; margin-bottom:2px;'>{o} — {prob*100:.1f}%</div>",
            unsafe_allow_html=True
        )
        st.progress(prob)

    st.write("Click a button to assign outcomes to players.")

    # --- Colour coding for results table ---
    def colour_outcomes(val):
        colours = {
            "Stay": "background-color: #c8f7c5; color: black;",
            "Out for the season": "background-color: #f7d4c5; color: black;",
            "Leaves": "background-color: #fce5cd; color: black;",
            "Dead": "background-color: #ffb3b3; color: black;",
            "Works weekends 1 in 4": "background-color: #fff2cc; color: black;",
            "Getting Married (Miss first 4 games)": "background-color: #d9d2e9; color: black;",
            "Lose 10 Skill Points": "background-color: #cfe2f3; color: black;"
        }
        return colours.get(val, "color: black;")

    # --- Session State for player assignment ---
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
            outcome = random.choices(
                outcomes,
                weights=[st.session_state.current_weights[o] for o in outcomes],
                k=1
            )[0]

            if outcome != "Stay":
                st.session_state.current_weights[outcome] = max(
                    1, st.session_state.current_weights[outcome] - 1
                )

            results.append({"Player": player, "Outcome": outcome})

        df_full = pd.DataFrame(results)
        df_full.index += 1
        st.session_state.full_results = df_full

    # --- Generate ONE Player ---
    if st.button("Generate One Player"):
        if st.session_state.remaining_players:
            player = random.choice(st.session_state.remaining_players)

            outcome = random.choices(
                outcomes,
                weights=[st.session_state.current_weights[o] for o in outcomes],
                k=1
            )[0]

            if outcome != "Stay":
                st.session_state.current_weights[outcome] = max(
                    1, st.session_state.current_weights[outcome] - 1
                )

            st.session_state.single_results.append({"Player": player, "Outcome": outcome})
            st.session_state.remaining_players.remove(player)
        else:
            st.warning("All players have already been assigned!")

    # --- RESET ---
    if st.button("Reset"):
        st.session_state.remaining_players = players.copy()
        st.session_state.single_results = []
        st.session_state.full_results = None

        st.session_state.current_weights = {
            "Stay": 70,
            "Out for the season": 5,
            "Leaves": 5,
            "Dead": 1,
            "Works weekends 1 in 4": 9,
            "Getting Married (Miss first 4 games)": 5,
            "Lose 10 Skill Points": 5
        }

        st.success("All data has been reset.")

    # --- Display Results ---
    if st.session_state.full_results is not None:
        st.subheader("All Player Outcomes")
        styled_full = st.session_state.full_results.style.applymap(colour_outcomes, subset=["Outcome"])
        st.dataframe(styled_full, use_container_width=True, height=600)

    if st.session_state.single_results:
        st.subheader("Assigned Players (One-by-One Mode)")
        df_single = pd.DataFrame(st.session_state.single_results)
        df_single.index += 1
        styled_single = df_single.style.applymap(colour_outcomes, subset=["Outcome"])
        st.dataframe(styled_single, use_container_width=True, height=600)
