import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Chiddingly Player Status", page_icon="🏏")

# ---------- STYLES ----------
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

/* Card-style panels */
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

/* Colour-coded outcomes */
.outcome-Stay { background-color: #c8f7c5; padding: 2px 4px; border-radius: 4px; }
.outcome-Out { background-color: #f7d4c5; padding: 2px 4px; border-radius: 4px; }
.outcome-Leaves { background-color: #fce5cd; padding: 2px 4px; border-radius: 4px; }
.outcome-Dead { background-color: #ffb3b3; padding: 2px 4px; border-radius: 4px; }
.outcome-Weekends { background-color: #fff2cc; padding: 2px 4px; border-radius: 4px; }
.outcome-Married { background-color: #d9d2e9; padding: 2px 4px; border-radius: 4px; }
.outcome-Skill { background-color: #cfe2f3; padding: 2px 4px; border-radius: 4px; }

/* Sticky button bar */
.sticky-bar {
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: #111;
    padding: 12px 10px;
    border-bottom: 1px solid #444;
}

/* Button spacing */
.stButton > button {
    margin-top: 5px;
    margin-bottom: 5px;
}
</style>
"""
st.markdown(page_css, unsafe_allow_html=True)

# ---------- DATA ----------
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

# ---------- STATE ----------
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

if "full_results" not in st.session_state:
    st.session_state.full_results = None

if "single_results" not in st.session_state:
    st.session_state.single_results = []

if "remaining_players" not in st.session_state:
    st.session_state.remaining_players = players.copy()

if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

if "modal_result" not in st.session_state:
    st.session_state.modal_result = None


# ---------- MODAL (st.dialog) ----------
@st.dialog("New Result")
def show_result_modal(player: str, outcome: str):
    st.markdown(
        f"""
        <p style='font-size:20px; margin:0; text-align:center;'><strong>{player}</strong></p>
        <p style='font-size:18px; margin-top:5px; text-align:center;'>
            Outcome: <strong>{outcome}</strong>
        </p>
        """,
        unsafe_allow_html=True,
    )

    st.write("")  # small spacer

    # Centered "Close" text button (A3-iii-1 style, but using Streamlit)
    cols = st.columns([1, 1, 1])
    with cols[1]:
        if st.button("Close"):
            st.session_state.show_modal = False
            st.session_state.modal_result = None
            st.rerun()


# ---------- LAYOUT ----------
left_col, mid_col, right_col = st.columns([0.8, 3.0, 0.8])

# LEFT COLUMN
with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Players</h3>", unsafe_allow_html=True)
    for p in players:
        st.markdown(f"<p class='player-name'>{p}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN
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

# MIDDLE COLUMN
with mid_col:
    header_left, header_mid, header_right = st.columns([1, 2, 1])
    with header_mid:
        st.image("twatsportz_logo.png", width=400)
        st.markdown(
            """
            <h1 style='text-align:center; margin-bottom: 20px;'>
                Chiddingly<br>Player Status Generator
            </h1>
            """,
            unsafe_allow_html=True
        )

    # Sticky bar
    st.markdown("<div class='sticky-bar'>", unsafe_allow_html=True)
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        all_clicked = st.button("Generate All Players")
    with btn2:
        one_clicked = st.button("Generate One Player")
    with btn3:
        reset_clicked = st.button("Reset All Players")
    st.markdown("</div>", unsafe_allow_html=True)

    # Probabilities
    st.markdown("<h3 style='text-align:center; margin-top:20px;'>Outcome Probabilities</h3>", unsafe_allow_html=True)
    total_weight = sum(st.session_state.current_weights[o] for o in outcomes)
    for o in outcomes:
        prob = st.session_state.current_weights[o] / total_weight
        st.markdown(
            f"<div style='font-size:15px; margin-bottom:2px;'>{o} — {prob*100:.1f}%</div>",
            unsafe_allow_html=True
        )
        st.progress(prob)

    # Logic
    if all_clicked:
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

    if one_clicked:
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

            result_entry = {"Player": player, "Outcome": outcome}
            st.session_state.single_results.append(result_entry)
            st.session_state.remaining_players.remove(player)

            st.session_state.modal_result = result_entry
            st.session_state.show_modal = True
        else:
            st.warning("All players have already been assigned!")

    if reset_clicked:
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
        st.session_state.show_modal = False
        st.session_state.modal_result = None
        st.success("All data has been reset.")

    # Tables
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

# Show modal if needed
if st.session_state.show_modal and st.session_state.modal_result is not None:
    show_result_modal(
        st.session_state.modal_result["Player"],
        st.session_state.modal_result["Outcome"],
    )
