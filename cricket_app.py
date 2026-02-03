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
    "Tim Crust", "Jimmy Tuckersmith", "Pat James",
    "William Withershaw", "Harvey Last",
    "Rob Akers", "Briddy Birgaminin", "Keith Hill", "Dom Pemberry"
]

outcomes = [
    "Stay",
    "Broke finger at work (Lose 10 fielding points)",
    "Broken Leg - Out for the season",
    "Confidence Crisis (Lose 5 Skill Points and gets new hairstyle)",
    "Getting Married (Miss first 4 games)",
    "Going through bad breakup (Lose 10 Skill Points)",
    "Leaves the club",
    "Private Coaching (Adds 5 Skill Points)",
    "Scouted by County (Adds 10 Skill points, misses first 2 games)",
    "Takes PED's (Max Strength and Agility)",
    "Works occasional weekends, misses 1 game in 4",
    "Dead",
]

# ---------- STATE ----------

if "current_weights" not in st.session_state:
    st.session_state.current_weights = {
        "Stay": 70,
        "Dead": 1,
        "Broke finger at work (Lose 10 fielding points)": 5,
        "Broken Leg - Out for the season": 5,
        "Confidence Crisis (Lose 5 Skill Points and gets new hairstyle)": 5,
        "Getting Married (Miss first 4 games)": 5,
        "Going through bad breakup (Lose 10 Skill Points)": 5,
        "Leaves the club": 5,
        "Private Coaching (Adds 5 Skill Points)": 5,
        "Scouted by County (Adds 10 Skill points, misses first 2 games)": 5,
        "Takes PED's (Max Strength and Agility)": 5,
        "Works occasional weekends, misses 1 game in 4": 5,
    }

if "single_results" not in st.session_state:
    st.session_state.single_results = []

if "remaining_players" not in st.session_state:
    st.session_state.remaining_players = players.copy()

if "show_modal" not in st.session_state:
    st.session_state.show_modal = False

if "modal_result" not in st.session_state:
    st.session_state.modal_result = None


# ---------- MODAL ----------

@st.dialog(" ")
def show_result_modal(player: str, outcome: str):

    st.markdown("""
        <style>
        .stDialog > div > div > div:nth-child(1) h1 {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style='text-align:center; margin-top:10px;'>
            <p style='font-size:36px; font-weight:bold; color:#FFD700; margin-bottom:5px;'>
                {player}
            </p>
            <p style='font-size:30px; font-weight:bold; color:#FFD700; margin-top:0;'>
                Outcome: {outcome}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cols = st.columns([1, 1, 1])
    with cols[1]:
        if st.button("Close", use_container_width=True):
            st.session_state.show_modal = False
            st.session_state.modal_result = None
            st.rerun()


# ---------- LAYOUT ----------

left_col, mid_col, right_col = st.columns([0.8, 3.0, 0.8])

# LEFT COLUMN – Players
with left_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Players</h3>", unsafe_allow_html=True)
    for p in players:
        st.markdown(f"<p class='player-name'>{p}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# RIGHT COLUMN – Outcomes
with right_col:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center; color:white;'>Outcomes</h3>", unsafe_allow_html=True)

    st.markdown("<p class='outcome-name outcome-Stay'>Stay</p>", unsafe_allow_html=True)

    st.markdown("<p class='outcome-name' style='background-color:#ffd9cc;'>Broke finger at work (Lose 10 fielding points)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Out'>Broken Leg - Out for the season</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name' style='background-color:#e6ccff;'>Confidence Crisis (Lose 5 Skill Points and gets new hairstyle)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Married'>Getting Married (Miss first 4 games)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Skill'>Going through bad breakup (Lose 10 Skill Points)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Leaves'>Leaves the club</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name' style='background-color:#d0f0c0;'>Private Coaching (Adds 5 Skill Points)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name' style='background-color:#cce6ff;'>Scouted by County (Adds 10 Skill points, misses first 2 games)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name' style='background-color:#fff2b3;'>Takes PED's (Max Strength and Agility)</p>", unsafe_allow_html=True)
    st.markdown("<p class='outcome-name outcome-Weekends'>Works occasional weekends, misses 1 game in 4</p>", unsafe_allow_html=True)

    st.markdown("<p class='outcome-name outcome-Dead'>Dead</p>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# MIDDLE COLUMN – Main UI
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
    btn_left, btn_mid, btn_right = st.columns([1, 1, 1])
    with btn_mid:
        one_clicked = st.button("Generate One Player", use_container_width=True)
        reset_clicked = st.button("Reset All Players", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------- GENERATE ONE PLAYER ----------
    if one_clicked:
        if st.session_state.remaining_players:

           # PICK PLAYER + OUTCOME
player = random.choice(st.session_state.remaining_players)
outcome = random.choices(
    outcomes,
    weights=[st.session_state.current_weights[o] for o in outcomes],
    k=1
)[0]

# Prevent Dom Pemberry and Briddy Birgaminin from leaving the club
if player in ["Dom Pemberry", "Briddy Birgaminin"] and outcome == "Leaves the club":
    outcome = "Stay"



            # UPDATE WEIGHTS
            if outcome != "Stay":
                st.session_state.current_weights[outcome] = max(
                    1, st.session_state.current_weights[outcome] - 1
                )

            # STORE RESULT
            result_entry = {"Player": player, "Outcome": outcome}
            st.session_state.single_results.append(result_entry)
            st.session_state.remaining_players.remove(player)

            # OPEN MODAL
            st.session_state.modal_result = result_entry
            st.session_state.show_modal = True

        else:
            st.warning("All players have already been assigned!")

    # ---------- RESET ----------
    if reset_clicked:
        st.session_state.remaining_players = players.copy()
        st.session_state.single_results = []
        st.session_state.current_weights = {
            "Stay": 70,
            "Dead": 1,
            "Broke finger at work (Lose 10 fielding points)": 5,
            "Broken Leg - Out for the season": 5,
            "Confidence Crisis (Lose 5 Skill Points and gets new hairstyle)": 5,
            "Getting Married (Miss first 4 games)": 5,
            "Going through bad breakup (Lose 10 Skill Points)": 5,
            "Leaves the club": 5,
            "Private Coaching (Adds 5 Skill Points)": 5,
            "Scouted by County (Adds 10 Skill points, misses first 2 games)": 5,
            "Takes PED's (Max Strength and Agility)": 5,
            "Works occasional weekends, misses 1 game in 4": 5,
        }
        st.session_state.show_modal = False
        st.session_state.modal_result = None
        st.success("All data has been reset.")

    # ---------- TABLE COLOURING ----------
    def colour_outcomes(val):
        colours = {
            "Stay": "background-color: #c8f7c5; color: black;",
            "Broken Leg - Out for the season": "background-color: #f7d4c5; color: black;",
            "Leaves the club": "background-color: #fce5cd; color: black;",
            "Dead": "background-color: #ffb3b3; color: black;",
            "Works occasional weekends, misses 1 game in 4": "background-color: #fff2cc; color: black;",
            "Getting Married (Miss first 4 games)": "background-color: #d9d2e9; color: black;",
            "Going through bad breakup (Lose 10 Skill Points)": "background-color: #cfe2f3; color: black;",
            "Private Coaching (Adds 5 Skill Points)": "background-color: #d0f0c0; color: black;",
            "Broke finger at work (Lose 10 fielding points)": "background-color: #ffd9cc; color: black;",
            "Confidence Crisis (Lose 5 Skill Points and gets new hairstyle)": "background-color: #e6ccff; color: black;",
            "Scouted by County (Adds 10 Skill points, misses first 2 games)": "background-color: #cce6ff; color: black;",
            "Takes PED's (Max Strength and Agility)": "background-color: #fff2b3; color: black;",
        }
        return colours.get(val, "color: black;")

    # ---------- RESULTS TABLE ----------
    if st.session_state.single_results:
        st.subheader("Assigned Players (One-by-One Mode)")
        df_single = pd.DataFrame(st.session_state.single_results)
        df_single.index += 1

        styled_single = df_single.style.applymap(colour_outcomes, subset=["Outcome"])

        styled_single = styled_single.set_table_styles([
            {"selector": "th.col_heading.level0.col0", "props": [("width", "120px")]},
            {"selector": "th.col_heading.level0.col1", "props": [("width", "600px")]},
            {"selector": "td.col0", "props": [("width", "120px")]},
            {"selector": "td.col1", "props": [("width", "600px")]}
        ])

        st.dataframe(styled_single, use_container_width=True, height=900)

# ---------- SHOW MODAL ----------
if st.session_state.show_modal and st.session_state.modal_result is not None:
    show_result_modal(
        st.session_state.modal_result["Player"],
        st.session_state.modal_result["Outcome"],
    )
