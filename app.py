import streamlit as st
import pandas as pd
import pickle
import papermill as pm
import os
import io
import base64
from PIL import Image
from streamlit.components.v1 import html
import warnings
import time
import random

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Doctor Finder Pro",
    layout="wide",
    page_icon="🏥",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "search"
if "search_params" not in st.session_state:
    st.session_state.search_params = {}
if "intro_animation_shown" not in st.session_state:
    st.session_state.intro_animation_shown = False

# --- Custom CSS ---
st.markdown(
    """
    <style>
/* Import only Dancing Script from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@400;700&display=swap');

/* Enhanced Background with a Professional Gradient and Subtle Medical Icons */
.stApp {
    background: linear-gradient(135deg, #F0F7FF 0%, #D6EAF8 100%);
    background-image: url("https://i.pinimg.com/originals/0e/80/3f/0e803ff6dbf0f871b957238c6e3df18b.gif");
    background-size: cover;
    background-position: center;
    font-family: 'Dancing Script', 'Georgia', serif !important;
    min-height: 100vh;
    position: relative;
    overflow: hidden; /* Ensure overlay doesn't overflow */
}

.stApp::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.6); /* Semi-transparent white overlay */
    z-index: 0; /* Behind content but above background */
}

.stApp > * {
    position: relative;
    z-index: 1; /* Ensure content stays above the overlay */
}

/* Animated Bubble Effects with Mixed Sizes and Darker Color */
.bubbles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: -1;
}
.bubble {
    position: absolute;
    bottom: -50px;
    background: rgba(0, 51, 153, 0.5); /* Even darker blue shade */
    border-radius: 50%;
    animation: float 6s infinite;
}
@keyframes float {
    0% { transform: translateY(0); opacity: 1; }
    100% { transform: translateY(-800px); opacity: 0; }
}

/* Animation Overlay */
.animation-overlay {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 100000 !important;
    background: white;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    align-items: center !important;
    overflow: visible !important;
}

/* Medical Icons at Corners and Edges */
.medical-icon {
    position: absolute !important;
    font-size: 3rem !important;
    color: #4B0082 !important; /* Match the new color scheme */
    opacity: 1 !important;
    z-index: 100001 !important;
    pointer-events: none !important;
    animation: sway 2s ease-in-out infinite !important;
}

/* Sway Animation for Left-to-Right Movement */
@keyframes sway {
    0% { transform: translateX(0); }
    50% { transform: translateX(20px); }
    100% { transform: translateX(0); }
}

/* Reverse Sway for Some Icons (Right-to-Left) */
.medical-icon.reverse-sway {
    animation: sway-reverse 2s ease-in-out infinite !important;
}

@keyframes sway-reverse {
    0% { transform: translateX(0); }
    50% { transform: translateX(-20px); }
    100% { transform: translateX(0); }
}

.welcome-content {
    text-align: center;
    z-index: 100002;
    position: relative;
}

.welcome-title {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: transparent !important;
    background: linear-gradient(90deg, #4B0082, #FF00FF) !important; /* New contrasting gradient */
    background-size: 200% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    animation: gradientMove 5s ease-in-out infinite, fadeIn 1s ease-out !important;
    margin-bottom: 1rem !important;
}

.welcome-subtitle {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 2.5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: #4B0082 !important; /* Dark purple for contrast */
    margin-bottom: 2rem !important;
    animation: fadeIn 1s 0.3s ease-out both !important;
}

.welcome-quote {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 2rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    font-style: italic !important;
    color: #FF00FF !important; /* Vibrant magenta for contrast */
    animation: fadeIn 1s 0.6s ease-out both !important;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Main Content Hidden During Animation */
.main-content-hidden {
    opacity: 0 !important;
    display: none !important;
    pointer-events: none !important;
}

/* Headings with new gradient */
h1, h2, h3 {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 3rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: transparent !important;
    text-align: center;
    margin: 1.5rem 0;
    background: linear-gradient(90deg, #8B0000, #FF6F61) !important; /* New contrasting gradient */
    background-size: 200% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    animation: gradientMove 5s ease-in-out infinite;
}

h1:hover, h2:hover, h3:hover {
    transform: scale(1.05);
}

/* Main heading with new gradient */
#d1a2c0fa {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: transparent !important;
    background: linear-gradient(to right, #3a0ca3, #00b37e) !important; /* New contrasting gradient */
    background-size: 200% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    animation: gradientMove 5s ease-in-out infinite, textEntrance 1.5s ease-out forwards !important;
    text-align: center !important;
}

@keyframes textEntrance {
    0% { opacity: 0; transform: translateY(20px); }
    100% { opacity: 1; transform: translateY(0); }
}

@keyframes gradientMove {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Hospital icon */
.hospital-icon {
    font-size: 5rem !important; /* Larger size */
    margin-right: 12px !important;
    display: inline-block !important;
    vertical-align: middle !important;
    animation: iconPulse 2s ease-in-out infinite;
}

@keyframes iconPulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.1); }
    100% { transform: scale(1); }
}

/* Custom labels for inputs */
.custom-label {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-weight: 700 !important; /* Bolder */
    font-size: 3rem !important; /* Larger size */
    color: transparent !important;
    background: linear-gradient(to right, #6a00f4, #ff1493) !important; /* New contrasting gradient */
    background-size: 200% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    animation: gradientMove 5s ease-in-out infinite !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin-bottom: 0.5rem !important;
}

.custom-label:hover {
    transform: scale(1.05);
}

.custom-label span {
    font-size: 3rem !important; /* Larger size */
    margin-right: 8px !important;
    background: none !important;
    -webkit-background-clip: initial !important;
    background-clip: initial !important;
    color: #4B0082 !important; /* Dark purple for contrast */
    animation: iconBeat 1.5s ease-in-out infinite !important;
}

@keyframes iconBeat {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

/* Hide default selectbox labels */
.stSelectbox label {
    display: none !important;
}

/* Select boxes with modern styling, increased width, padding, and font size */
div[data-baseweb="select"] {
    background: linear-gradient(90deg, #BAE6FD, #E0F7FA);
    border: 2px solid #4B0082; /* Match new color scheme */
    border-radius: 10px;
    padding: 15px 40px 15px 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 450px;
    margin: 0 auto;
    transition: all 0.3s ease;
    overflow: visible;
    min-height: 60px;
    display: flex;
    align-items: center;
}

div[data-baseweb="select"]:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-color: #FF00FF; /* Match new color scheme */
    transform: scale(1.03);
}

div[data-baseweb="select"] > div {
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
}

div[data-baseweb="select"] > div > div > div {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 2.5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: #4B0082 !important; /* Dark purple for contrast */
    line-height: 1.5;
}

/* Dropdown items with increased font size and proper spacing */
ul[data-testid="stSelectboxVirtualDropdown"] {
    max-height: 300px;
    overflow-y: auto;
}

ul[data-testid="stSelectboxVirtualDropdown"] li {
    background: linear-gradient(90deg, #BAE6FD, #E0F7FA);
    border-radius: 15px;
    padding: 15px 20px;
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 2.2rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    color: #4B0082 !important; /* Dark purple for contrast */
    white-space: normal;
    overflow: visible;
    text-overflow: unset;
    min-height: 50px;
    display: flex;
    align-items: center;
}

ul[data-testid="stSelectboxVirtualDropdown"] li:hover {
    background: linear-gradient(90deg, #A5F3FC, #BAE6FD);
    transform: scale(1.03);
}

/* Search button with elegant fill and unfill animation */
.stButton > button {
    background: white;
    border: 2px solid #4B0082; /* Match new color scheme */
    border-radius: 25px;
    padding: 15px 30px;
    color: linear-gradient(to right, #ff416c, #ffaf00) !important; /* Dark purple for contrast */
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 2.5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
    width: 200px;
    margin: 1rem auto;
    display: block;
    position: relative;
    overflow: hidden;
    animation: fillUnfill 4s ease-in-out infinite, glow 4s ease-in-out infinite;
}

/* Automatic fill and unfill animation with softer yellowish-gold */
@keyframes fillUnfill {
    0% { background: white; }
    50% { background: linear-gradient(90deg, #FFD700, #FFECB3); }
    100% { background: white; }
}

/* Subtle glow animation */
@keyframes glow {
    0% { box-shadow: 0 0 10px rgba(75, 0, 130, 0.5); } /* Match new color scheme */
    50% { box-shadow: 0 0 20px rgba(255, 215, 0, 0.6); }
    100% { box-shadow: 0 0 10px rgba(75, 0, 130, 0.5); } /* Match new color scheme */
}

/* Remove the ::before pseudo-element */
.stButton > button::before {
    display: none;
}

/* Click-to-vanish effect */
.stButton > button:active {
    animation: vanish 0.5s forwards;
}

@keyframes vanish {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.2); }
    100% { opacity: 0; transform: scale(0); }
}

/* Tables */
.stDataFrame {
    width: 70%;
    margin: 2rem auto;
    border: 2px solid #FF00FF; /* Match new color scheme */
    border-radius: 15px;
    background: rgba(255, 255, 255, 0.9);
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.7);
}

.stDataFrame th {
    background: linear-gradient(90deg, #4B0082, #FF00FF); /* Match new color scheme */
    color: white;
    padding: 16px;
}

.stDataFrame td {
    padding: 14px;
    border-bottom: 1px solid #E0F7FA;
    color: #4B0082 !important; /* Match new color scheme */
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 1.5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
}

.stDataFrame tr:hover td {
    background: #E0F7FA;
}

/* Scrollable card */
.scrollable-card {
    max-height: 400px;
    overflow-y: auto;
    border: 2px solid #FF00FF; /* Match new color scheme */
    border-radius: 10px;
    padding: 10px;
    margin: 0 auto;
}

/* Center content */
.stApp > div {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-height: 100vh;
    padding: 2rem;
}

/* Loading GIF */
.loading-gif-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: white;
    z-index: 20000;
}

.loading-gif {
    max-width: 80%;
    max-height: 80%;
}

/* Ensure body text uses Dancing Script */
p, div, span {
    font-family: 'Dancing Script', 'Georgia', serif !important;
    font-size: 1.5rem !important; /* Larger size */
    font-weight: 700 !important; /* Bolder */
}
</style>
<div class="bubbles">
    <div class="bubble" style="left: 5%; width: 40px; height: 40px; animation-duration: 5s;"></div>
    <div class="bubble" style="left: 15%; width: 10px; height: 10px; animation-duration: 6s;"></div>
    <div class="bubble" style="left: 25%; width: 25px; height: 25px; animation-duration: 4s;"></div>
    <div class="bubble" style="left: 35%; width: 40px; height: 40px; animation-duration: 7s;"></div>
    <div class="bubble" style="left: 45%; width: 10px; height: 10px; animation-duration: 5s;"></div>
    <div class="bubble" style="left: 55%; width: 25px; height: 25px; animation-duration: 6s;"></div>
    <div class="bubble" style="left: 65%; width: 40px; height: 40px; animation-duration: 4s;"></div>
    <div class="bubble" style="left: 75%; width: 10px; height: 10px; animation-duration: 7s;"></div>
    <div class="bubble" style="left: 85%; width: 25px; height: 25px; animation-duration: 5s;"></div>
    <div class="bubble" style="left: 95%; width: 40px; height: 40px; animation-duration: 6s;"></div>
</div>
""",
    unsafe_allow_html=True
)

# --- Navigation Functions ---
def go_to_loading(params):
    st.session_state.search_params = params
    st.session_state.page = "loading"
    st.rerun()

def go_to_results():
    st.session_state.page = "results"
    st.rerun()

# --- Search Page ---        
if st.session_state.page == "search":
    if not st.session_state.intro_animation_shown:
        # Show a warning about font loading
        st.warning("If fonts don’t load properly, please disable browser tracking prevention or allow access to fonts.gstatic.com for the best experience.")

        # Inject animation HTML with adjusted topmost icons
        st.markdown("""
        <div class="animation-overlay" id="animationOverlay">
            <div class="welcome-content">
                <div style="font-size: 5rem; animation: iconPulse 2s infinite;">🏥</div>
                <div class="welcome-title">Doctor Finder Pro</div>
                <div class="welcome-subtitle">Your trusted medical specialist finder</div>
                <div class="welcome-quote">"We'll find the perfect doctor for your needs"</div>
            </div>
            <div class="medical-icon sway" style="left: 20px; top: 40px;">💉</div>
            <div class="medical-icon sway-reverse" style="right: 20px; top: 40px;">🩺</div>
            <div class="medical-icon sway" style="left: 25%; top: 40px;">🌡️</div>
            <div class="medical-icon sway-reverse" style="left: 50%; top: 40px;">🩹</div>
            <div class="medical-icon sway" style="left: 75%; top: 40px;">💗</div>
            <div class="medical-icon sway-reverse" style="left: 25%; bottom: 20px;">🔬</div>
            <div class="medical-icon sway" style="left: 50%; bottom: 20px;">🩺</div>
            <div class="medical-icon sway-reverse" style="left: 75%; bottom: 20px;">💉</div>
            <div class="medical-icon sway" style="left: 20px; top: 25%;">🩹</div>
            <div class="medical-icon sway-reverse" style="left: 20px; top: 50%;">💗</div>
            <div class="medical-icon sway" style="left: 20px; top: 75%;">🌡️</div>
            <div class="medical-icon sway-reverse" style="right: 20px; top: 25%;">🔬</div>
            <div class="medical-icon sway" style="right: 20px; top: 50%;">💊</div>
            <div class="medical-icon sway-reverse" style="right: 20px; top: 75%;">😷</div>
            <div class="medical-icon sway" style="left: 20px; bottom: 20px;">💊</div>
            <div class="medical-icon sway-reverse" style="right: 20px; bottom: 20px;">😷</div>
        </div>

        <script>
            // Hide main content during animation
            const mainContent = document.querySelector(".stApp") || document.querySelector("main");
            if (mainContent) {
                mainContent.classList.add("main-content-hidden");
            }

            // Fade out overlay after animation
            setTimeout(() => {
                const overlay = document.getElementById('animationOverlay');
                if (overlay) {
                    overlay.style.transition = 'opacity 0.5s ease';
                    overlay.style.opacity = '0';
                    overlay.style.pointerEvents = 'none';

                    if (mainContent) {
                        mainContent.classList.remove("main-content-hidden");
                        mainContent.style.transition = 'opacity 0.5s ease';
                        mainContent.style.opacity = '1';
                    }

                    setTimeout(() => {
                        overlay.style.display = 'none';
                    }, 500);
                }
            }, 3500);
        </script>
        """, unsafe_allow_html=True)

        # Wait for animation to complete
        time.sleep(4)
        st.session_state.intro_animation_shown = True
        st.rerun()
    else:
        # Main content
        st.markdown("""
        <h1 class="main-title-with-icon">
            <span class="hospital-icon">🏥</span>
            <span class="title-text" id="d1a2c0fa">Doctor Finder Pro</span>
        </h1>
        """, unsafe_allow_html=True)
        st.markdown("""
        <p style='text-align: center; color: #4B0082; font-size: 1.5rem; font-weight: 700; margin-bottom: 2rem;'>
        Find the perfect medical specialist with our advanced search system
        </p>
        """, unsafe_allow_html=True)

        # --- Load Data ---
        @st.cache_data
        def load_data():
            return pd.read_excel("panel_data.xlsx", parse_dates=False)

        df = load_data()
        specialities = df['Speciality'].unique()
        regions = ['All Regions'] + list(df['Region'].unique())

        # --- Inputs ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<div class="custom-label"><span>🩺</span>Speciality (required)</div>', unsafe_allow_html=True)
            speciality = st.selectbox("select", specialities, label_visibility="hidden")
        with col2:
            st.markdown('<div class="custom-label"><span>📍</span>Region (optional)</div>', unsafe_allow_html=True)
            region = st.selectbox("select", regions, index=0, label_visibility="hidden")

        # --- Search Button ---
        if st.button("🔎 Search"):
            params = {"speciality": speciality, "region": region if region != 'All Regions' else "All_Regions"}
            go_to_loading(params)

# --- Loading Page ---
elif st.session_state.page == "loading":
    st.markdown(
        """
        <div class="loading-gif-container">
            <img src="https://cdn.dribbble.com/userupload/42285428/file/original-b772875e09fd1af0b0fe3d69eae44dfa.gif" class="loading-gif">
        </div>
        """,
        unsafe_allow_html=True
    )

    # Execute notebook
    params = st.session_state.search_params
    try:
        pm.execute_notebook("test2.ipynb", "output1.ipynb", parameters=params, kernel_name="python3")
    except Exception as e:
        st.session_state.error = f"Error executing notebook: {str(e)}"
        go_to_results()
        st.stop()

    try:
        with open('output.pkl', 'rb') as f:
            st.session_state.results = pickle.load(f)
    except FileNotFoundError:
        st.session_state.error = "Output file 'output.pkl' not found."
        go_to_results()
        st.stop()

    # Simulate loading delay
    time.sleep(2)
    go_to_results()

# --- Results Page ---
elif st.session_state.page == "results":
    st.title("🏥 Doctor Finder Pro - Results")
    
    # Check for errors
    if "error" in st.session_state:
        st.error(st.session_state.error)
        st.stop()

    regions_df_list, region_names, region_wise_percent, visualization_files = st.session_state.results
    speciality = st.session_state.search_params["speciality"]
    region = st.session_state.search_params["region"] if st.session_state.search_params["region"] != "All_Regions" else "All Regions"

    # --- Display Matching Doctors ---
    st.subheader("📋 Matching Doctors")
    if sum(len(df) for df in regions_df_list) == 0:
        st.warning(f"No doctors found for speciality: {speciality}")
    else:
        for region_df, region_name in zip(regions_df_list, region_names):
            if not region_df.empty:
                st.markdown(f"**{region_name}**")
                st.markdown('<div class="scrollable-card">', unsafe_allow_html=True)
                st.dataframe(region_df[['NPI', 'State', 'Usage Time (mins)', 'Region', 'Speciality']], use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.write(f"No data for {speciality} in {region_name}")

    # --- Display Region-Wise Percentages ---
    st.subheader("📊 Region-Wise Distribution")
    percent_df = pd.DataFrame({"Region": region_names, "Percentage": region_wise_percent})
    st.dataframe(percent_df, use_container_width=True)

    # --- Display Plots ---
    def image_to_base64(img):
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode()
        return img_b64

    st.subheader("📈 Analysis Plots")

    plot_names = {
        "npi_by_region": f"Number of {speciality} NPIs by Region",
        "npi_by_state": f"Number of {speciality} NPIs by State",
        "usage_by_region": f"Average Usage Time for {speciality} by Region",
        "usage_distribution": f"Distribution of Usage Time for {speciality}",
        "usage_boxplot": f"Usage Time Distribution by Region for {speciality}",
        "npi_heatmap": f"Heatmap of {speciality} NPIs by State and Region",
        "top_states_usage": f"Top 10 States by Average Usage Time for {speciality}",
        "regional_pie": f"Regional Distribution of {speciality} NPIs"
    }
    if region != "All Regions":
        plot_names.update({
            "npi_by_state_region": f"Number of {speciality} NPIs by State in {region}",
            "usage_by_state_region": f"Average Usage Time for {speciality} by State in {region}",
            "usage_distribution_region": f"Distribution of Usage Time for {speciality} in {region}",
            "state_pie_region": f"Distribution of {speciality} NPIs by State in {region}",
            "top_npis_region": f"Top 10 {speciality} NPIs in {region} by Usage Time",
            "usage_thresholds_region": f"Percentage of {speciality} NPIs in {region} Above Usage Time Thresholds"
        })

    plot_keys = [key for key, file in visualization_files.items() if file.endswith(".png")]

    # Loop through plots and show two per row
    for i in range(0, len(plot_keys), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(plot_keys):
                key = plot_keys[i + j]
                title = plot_names.get(key, key)
                try:
                    img = Image.open(visualization_files[key])
                    img_b64 = image_to_base64(img)
                    html_code = f'''
                    <div class="plot-card">
                        <img src="data:image/png;base64,{img_b64}" />
                        <p>{title}</p>
                    </div>
                    '''
                    with cols[j]:
                        st.markdown(html_code, unsafe_allow_html=True)
                except FileNotFoundError:
                    with cols[j]:
                        st.warning(f"Plot file {visualization_files[key]} not found.")

    # --- Display Maps ---
    st.subheader("🗺️ Interactive Maps")
    map_names = {
        "choropleth_map": f"Distribution of {speciality} NPIs Across US States",
        "region_bar": f"NPI Distribution by {'State' if region != 'All Regions' else 'Region'}",
        "region_pie": f"Percentage Distribution of {speciality} NPIs",
        "usage_bar": f"Average Usage Time by {'State' if region != 'All Regions' else 'Region'}",
        "state_heatmap": f"Comprehensive NPI Distribution Map for {speciality}"
    }
    for key, title in map_names.items():
        if key in visualization_files and visualization_files[key].endswith(".html"):
            try:
                with open(visualization_files[key], "r") as f:
                    html_content = f.read()
                st.markdown(f"**{title}**")
                html(html_content, height=600)
            except FileNotFoundError:
                st.warning(f"Map file {visualization_files[key]} not found.")

    # --- Display NPI Count Data ---
    if "count_data" in visualization_files:
        try:
            count_data = pd.read_csv(visualization_files["count_data"])
            st.subheader("📋 NPI Count Summary")
            st.dataframe(count_data, use_container_width=True)
        except FileNotFoundError:
            st.warning("NPI count data file not found.")

    # --- Back to Search Button ---
    if st.button("🔙 Back to Search"):
        st.session_state.page = "search"
        if "results" in st.session_state:
            del st.session_state.results
        if "error" in st.session_state:
            del st.session_state.error
        st.rerun()
