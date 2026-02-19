from datetime import datetime
import streamlit as st
import pandas as pd
import io
import zipfile
import base64
import json
from app import load_schedule, load_race_results, get_driver_standings, get_circuit_info, get_constructor_results, get_constructor_standings, get_constructors_data, get_drivers_data, get_lap_times, get_pit_stops, get_qualifying_results, get_races_data, get_season_data, get_sprint_results, get_status_data

# Add background image
def add_bg_from_local(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("data:image/avif;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
        }}
        .title {{
            text-align: center;
            padding: 20px;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Set page config and background
st.set_page_config(layout="wide")
add_bg_from_local('images/f1.avif')

st.sidebar.markdown(
    "<h1 style='color: #FF1E00; font-weight: bold; font-size: 48px;'>F1RDF 🏎️</h1>", 
    unsafe_allow_html=True
)

# Add New Chat button
if st.sidebar.button("Home", key="new_chat", type="secondary", use_container_width=True):
    st.session_state.data_fetched = False
    st.session_state.fetched_data = {}
    st.rerun()

# Update F1 races list (remove round numbers from names)
f1_races = [
    "Australian Grand Prix",
    "Chinese Grand Prix",
    "Japanese Grand Prix",
    "Bahrain Grand Prix",
    "Saudi Arabian Grand Prix",
    "Miami Grand Prix",
    "Emilia Romagna Grand Prix",
    "Monaco Grand Prix",
    "Spanish Grand Prix",
    "Canadian Grand Prix",
    "Austrian Grand Prix",
    "British Grand Prix",
    "Belgian Grand Prix",
    "Hungarian Grand Prix",
    "Dutch Grand Prix",
    "Italian Grand Prix",
    "Azerbaijan Grand Prix",
    "Singapore Grand Prix",
    "United States Grand Prix",
    "Mexico City Grand Prix",
    "São Paulo Grand Prix",
    "Las Vegas Grand Prix",
    "Qatar Grand Prix",
    "Abu Dhabi Grand Prix"
]

def convert_to_serializable(obj):
    """Convert non-serializable objects to serializable format"""
    if pd.isna(obj):
        return None
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convert_to_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_serializable(item) for item in obj]
    else:
        return obj

def main():
    # Initialize session state first
    if 'data_fetched' not in st.session_state:
        st.session_state.data_fetched = False
    if 'fetched_data' not in st.session_state:
        st.session_state.fetched_data = {}
    if 'selected_year' not in st.session_state:
        st.session_state.selected_year = None
    if 'selected_race' not in st.session_state:
        st.session_state.selected_race = None
    if 'selected_round' not in st.session_state:
        st.session_state.selected_round = None
    if 'select_all' not in st.session_state:
        st.session_state.select_all = False
    if 'active_view' not in st.session_state:
        st.session_state.active_view = 'fetcher'

    st.markdown("<h1 class='title'>Formula 1 Race Data Fetcher</h1>", unsafe_allow_html=True)

    toggle_col1, toggle_col2 = st.columns(2)
    with toggle_col1:
        fetcher_type = "primary" if st.session_state.active_view == 'fetcher' else "secondary"
        if st.button("Data Fetcher", key="view_fetcher", type=fetcher_type, use_container_width=True):
            st.session_state.active_view = 'fetcher'
            st.rerun()
    with toggle_col2:
        calendar_type = "primary" if st.session_state.active_view == 'calendar' else "secondary"
        if st.button("Race Calendar", key="view_calendar", type=calendar_type, use_container_width=True):
            st.session_state.active_view = 'calendar'
            st.rerun()
    st.markdown("---")
    
    # Sidebar with year selection
    with st.sidebar:
        st.header("Race Selection")
        current_year = datetime.now().year
        default_year = current_year - 1 if current_year == 2026 else current_year
        year = st.selectbox("Select Year", range(default_year, 1950, -1), index=0)
        
        # Load schedule for selected year
        try:
            schedule = load_schedule(year)
        except ValueError:
            st.error(f"Schedule data not available for {year}. Please select a different year.")
            return
        
        available_races = schedule['EventName'].tolist()
        filtered_races = [race for race in f1_races if any(race.lower() in ar.lower() for ar in available_races)]
        
        if not filtered_races:
            filtered_races = available_races
        
        selected_race_name = st.selectbox("Select Grand Prix", filtered_races)
        
        round_number = None
        if selected_race_name:
            race_info = schedule[schedule['EventName'] == selected_race_name]
            if not race_info.empty:
                round_number = race_info.iloc[0]['RoundNumber']

        st.sidebar.markdown("")
        st.sidebar.markdown("## About")
        st.sidebar.info("This app fetches Formula 1 racing data from 1950 to present. Select a year and Grand Prix to access detailed race information including results, standings, lap times, pit stops, and more. You can download any data table as a CSV file.")

        st.sidebar.markdown("")
        st.sidebar.markdown("<h1 style='color: #00A1E8; font-weight: bold; font-size: 20px;'>Built by Umer Haddii</h1>", 
    unsafe_allow_html=True)
        
        linkedin = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/linkedin.gif"
        kaggle = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/kaggle.gif"
        share = "https://raw.githubusercontent.com/umerhaddii/stocky/main/images/share.gif"

        st.sidebar.caption(
        f"""
            <div style='display: flex; align-items: center;'>
                <a href = 'https://www.linkedin.com/in/umerhaddii'><img src='{linkedin}' style='width: 40px; height: 40px; margin-right: 25px;'></a>
                <a href = 'https://www.kaggle.com/umerhaddii'><img src='{kaggle}' style='width: 40px; height: 40px; margin-right: 25px;'></a>
                <a href = 'https://linktr.ee/umerhaddii'><img src='{share}' style='width: 40px; height: 40px; margin-right: 25px;'></a>
            
            </div>
            """,
        unsafe_allow_html=True,)

    # Check if selection changed - if yes, reset data_fetched
    if (st.session_state.selected_year != year or 
        st.session_state.selected_race != selected_race_name):
        st.session_state.data_fetched = False
        st.session_state.fetched_data = {}
        st.session_state.selected_year = year
        st.session_state.selected_race = selected_race_name
        st.session_state.selected_round = round_number
        st.session_state.select_all = False

    # Main Content Area — Calendar view
    if st.session_state.active_view == 'calendar':
        st.subheader(f"Race Calendar - {year}")
        schedule_df = schedule[['RoundNumber', 'EventName', 'Country', 'EventDate', 'Location']]
        st.dataframe(schedule_df, use_container_width=True)

    # Main Content Area — Data Fetcher view
    elif st.session_state.active_view == 'fetcher':
        if not st.session_state.data_fetched:
            if selected_race_name and round_number:
                sections = [
                    ("Race Results", "🏁", "race_results"),
                    ("Driver Standings", "🎖", "driver_standings"),
                    ("Circuits Data", "🏁", "circuit_info"),
                    ("Constructor Results", "🏆", "constructor_results"),
                    ("Constructor Standings", "📊", "constructor_standings"),
                    ("Constructors Data", "🏗", "constructors_data"),
                    ("Drivers Data", "👨‍✈️", "drivers_data"),
                    ("Lap Times", "⏱", "lap_times"),
                    ("Pit Stops Data", "🔧", "pit_stops"),
                    ("Qualifying Results", "⏳", "qualifying_results"),
                    ("Races Data", "🚥", "races_data"),
                    ("Season Data", "📅", "season_data"),
                    ("Sprint Race Results", "⚡", "sprint_results"),
                    ("Status Data (Race Completion Status)", "✅", "status_data")
                ]

                st.markdown("### Select Data Sections to Fetch")

                col1, col2 = st.columns(2)
                selected_sections = {}

                mid_point = len(sections) // 2
                for i, (name, icon, key) in enumerate(sections):
                    col = col1 if i < mid_point else col2
                    with col:
                        selected_sections[key] = st.checkbox(
                            f"{icon} {name}",
                            key=f"check_{key}",
                            value=st.session_state.select_all
                        )

                st.markdown("")
                selected_count = sum(selected_sections.values())
                btn_col1, btn_col2 = st.columns(2)

                with btn_col1:
                    if st.button("Select All", key="select_all_btn", use_container_width=True):
                        st.session_state.select_all = not st.session_state.select_all
                        for _, _, k in sections:
                            if f"check_{k}" in st.session_state:
                                del st.session_state[f"check_{k}"]
                        st.rerun()

                with btn_col2:
                    fetch_label = f"🚀 Fetch Selected Data ({selected_count})" if selected_count > 0 else "🚀 Fetch Selected Data"
                    if st.button(fetch_label, key="fetch_btn", type="primary", use_container_width=True):
                        if not any(selected_sections.values()):
                            st.warning("Please select at least one data section to fetch.")
                        else:
                            with st.spinner('🏎️ Fetching race data...'):
                                progress_bar = st.progress(0)
                                total_sections = sum(selected_sections.values())
                                completed = 0

                                fetch_functions = {
                                    "race_results": lambda: load_race_results(year, round_number),
                                    "driver_standings": lambda: get_driver_standings(year, round_number),
                                    "circuit_info": lambda: get_circuit_info(year, round_number),
                                    "constructor_results": lambda: get_constructor_results(year, round_number),
                                    "constructor_standings": lambda: get_constructor_standings(year, round_number),
                                    "constructors_data": lambda: get_constructors_data(year, round_number),
                                    "drivers_data": lambda: get_drivers_data(year, round_number),
                                    "lap_times": lambda: get_lap_times(year, round_number),
                                    "pit_stops": lambda: get_pit_stops(year, round_number),
                                    "qualifying_results": lambda: get_qualifying_results(year, round_number),
                                    "races_data": lambda: get_races_data(year),
                                    "season_data": lambda: get_season_data(year),
                                    "sprint_results": lambda: get_sprint_results(year, round_number),
                                    "status_data": lambda: get_status_data(year, round_number)
                                }

                                for key, is_selected in selected_sections.items():
                                    if is_selected:
                                        try:
                                            st.session_state.fetched_data[key] = fetch_functions[key]()
                                            completed += 1
                                            progress_bar.progress(completed / total_sections)
                                        except Exception as e:
                                            st.session_state.fetched_data[key] = f"Error: {str(e)}"
                                            completed += 1
                                            progress_bar.progress(completed / total_sections)

                                progress_bar.empty()
                                st.session_state.data_fetched = True
                                st.session_state.select_all = False
                                st.rerun()

        if st.session_state.data_fetched and st.session_state.fetched_data:
            col1, col2 = st.columns([1, 1])

            with col1:
                if st.button("🔄 Fetch Different Data", type="secondary", use_container_width=True):
                    st.session_state.data_fetched = False
                    st.session_state.fetched_data = {}
                    st.session_state.select_all = False
                    st.rerun()

            with col2:
                if len(st.session_state.fetched_data) >= 1:
                    zip_buffer = io.BytesIO()
                    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                        for key, data in st.session_state.fetched_data.items():
                            if not (isinstance(data, str) and data.startswith("Error")) and data is not None:
                                if isinstance(data, dict):
                                    serializable_data = convert_to_serializable(data)
                                    json_data = json.dumps(serializable_data, indent=2)
                                    zip_file.writestr("circuit_info.json", json_data)
                                else:
                                    csv_data = data.to_csv(index=False)
                                    section_titles_map = {
                                        "race_results": "race_results.csv",
                                        "driver_standings": "driver_standings.csv",
                                        "circuit_info": "circuit_info.json",
                                        "constructor_results": "constructor_results.csv",
                                        "constructor_standings": "constructor_standings.csv",
                                        "constructors_data": "constructors_data.csv",
                                        "drivers_data": "drivers_data.csv",
                                        "lap_times": "lap_times.csv",
                                        "pit_stops": "pit_stops.csv",
                                        "qualifying_results": "qualifying_results.csv",
                                        "races_data": "races_data.csv",
                                        "season_data": "season_data.csv",
                                        "sprint_results": "sprint_results.csv",
                                        "status_data": "status_data.csv"
                                    }
                                    filename = section_titles_map.get(key, f"{key}.csv")
                                    zip_file.writestr(filename, csv_data)

                    zip_buffer.seek(0)
                    st.download_button(
                        label="📦 Download All Files (ZIP)",
                        data=zip_buffer.getvalue(),
                        file_name=f"F1_Data_{st.session_state.selected_year}_{st.session_state.selected_race.replace(' ', '_')}.zip",
                        mime="application/zip",
                        type="primary",
                        use_container_width=True,
                        key="download_all_zip"
                    )

            n = len(st.session_state.fetched_data)
            st.caption(f"✅ {n} dataset(s) fetched for {st.session_state.selected_race} {st.session_state.selected_year}")

            st.markdown("---")

            section_titles = {
                "race_results": ("🏁 Race Results", "race_results.csv"),
                "driver_standings": ("🎖 Driver Standings", "driver_standings.csv"),
                "circuit_info": ("🏁 Circuit Information", "circuit_info.json"),
                "constructor_results": ("🏆 Constructor Results", "constructor_results.csv"),
                "constructor_standings": ("📊 Constructor Standings", "constructor_standings.csv"),
                "constructors_data": ("🏗 Constructors Data", "constructors_data.csv"),
                "drivers_data": ("👨‍✈️ Drivers Data", "drivers_data.csv"),
                "lap_times": ("⏱ Lap Times", "lap_times.csv"),
                "pit_stops": ("🔧 Pit Stops Data", "pit_stops.csv"),
                "qualifying_results": ("⏳ Qualifying Results", "qualifying_results.csv"),
                "races_data": ("🚥 Races Data", "races_data.csv"),
                "season_data": ("📅 Season Data", "season_data.csv"),
                "sprint_results": ("⚡ Sprint Race Results", "sprint_results.csv"),
                "status_data": ("✅ Status Data", "status_data.csv")
            }

            for key, data in st.session_state.fetched_data.items():
                if key in section_titles:
                    title, filename = section_titles[key]
                    with st.expander(title, expanded=False):
                        if isinstance(data, str) and data.startswith("Error"):
                            st.error(data)
                        elif data is None:
                            st.info("No data available for this section.")
                        elif isinstance(data, dict):
                            serializable_data = convert_to_serializable(data)
                            for k, v in serializable_data.items():
                                if isinstance(v, dict):
                                    st.write(f"**{k.replace('_', ' ').title()}:**")
                                    st.json(v)
                                else:
                                    st.write(f"**{k.replace('_', ' ').title()}:** {v}")
                            json_data = json.dumps(serializable_data, indent=2)
                            st.download_button(
                                label=f"📥 Download {title}",
                                data=json_data,
                                file_name=filename,
                                mime="application/json",
                                key=f"download_{key}",
                                use_container_width=True
                            )
                        else:
                            st.dataframe(data, use_container_width=True)
                            csv = data.to_csv(index=False)
                            st.download_button(
                                label=f"📥 Download {title}",
                                data=csv,
                                file_name=filename,
                                mime="text/csv",
                                key=f"download_{key}",
                                use_container_width=True
                            )

if __name__ == '__main__':
    main()


