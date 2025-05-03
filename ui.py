import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from app import load_schedule, load_race_results, get_driver_standings, get_circuit_info, get_constructor_results, get_constructor_standings, get_constructors_data, get_drivers_data, get_lap_times, get_pit_stops, get_qualifying_results, get_races_data, get_season_data, get_sprint_results, get_status_data
import pandas as pd
import base64

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

def main():
    st.markdown("<h1 class='title'>Formula 1 Race Data Fetcher</h1>", unsafe_allow_html=True)
    
    # Initialize session state for fetched data only
    if 'data_fetched' not in st.session_state:
        st.session_state.data_fetched = False
    
    # Sidebar with year selection
    with st.sidebar:
        st.header("Race Selection")
        current_year = datetime.now().year
        year = st.selectbox("Select Year", range(current_year, 1950, -1))
        
        # Load schedule for selected year
        schedule = load_schedule(year)
        available_races = schedule['EventName'].tolist()
        filtered_races = [race for race in f1_races if any(race.lower() in ar.lower() for ar in available_races)]
        
        if not filtered_races:
            filtered_races = available_races
        
        selected_race_name = st.selectbox("Select Grand Prix", filtered_races)
        
        if selected_race_name:
            race_info = schedule[schedule['EventName'] == selected_race_name]
            if not race_info.empty:
                selected_round = race_info['RoundNumber'].iloc[0]

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

    # Main Content Area
    if not st.session_state.data_fetched:
        # Display race calendar
        st.subheader(f"Race Calendar - {year}")
        schedule_df = schedule[['RoundNumber', 'EventName', 'Country', 'EventDate', 'Location']]
        st.dataframe(schedule_df)

        if selected_race_name:  # Only show sections if a race is selected
            # List of all available data sections with icons
            sections = [
                ("Circuits Data", "🏁"),
                ("Constructor Results", "🏆"),
                ("Constructor Standings", "📊"),
                ("Constructors Data", "🏗"),
                ("Driver Standings", "🎖"),
                ("Drivers Data", "👨‍✈️"),
                ("Lap Times", "⏱"),
                ("Pit Stops Data", "🔧"),
                ("Qualifying Results", "⏳"),
                ("Races Data", "🚥"),
                ("Race Results", "🏁"),
                ("Season Data", "📅"),
                ("Sprint Race Results", "⚡"),
                ("Status Data (Race Completion Status)", "✅")
            ]

            # Split sections into two halves
            midpoint = len(sections) // 2
            left_sections = sections[:midpoint]
            right_sections = sections[midpoint:]

            # Create a form for batch selection
            with st.form("data_selection_form"):
                st.subheader("Select Data Sections to Fetch")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    left_selected_sections = {section: st.checkbox(f"{icon} {section}") 
                                           for section, icon in left_sections}
                
                with col2:
                    right_selected_sections = {section: st.checkbox(f"{icon} {section}") 
                                            for section, icon in right_sections}
                
                fetch_button = st.form_submit_button("Fetch Selected Data")

                if fetch_button:
                    selected_sections = {**left_selected_sections, **right_selected_sections}
                    st.session_state.selected_sections = selected_sections
                    st.session_state.data_fetched = True
                    st.session_state.year = year
                    st.session_state.selected_round = selected_round
                    st.rerun()

    # Main content - only show when data is fetched
    if st.session_state.data_fetched:
        with st.spinner('Fetching race data...'):
            try:
                year = st.session_state.year
                selected_round = st.session_state.selected_round
                
                # Add Constructor Results section
                if st.session_state.selected_sections.get('Constructor Results', False):
                    st.subheader("Constructor Results")
                    constructor_results = get_constructor_results(year, selected_round)
                    st.dataframe(constructor_results)
                    
                    # Add download button for constructor results
                    csv_constructor = constructor_results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Constructor Results",
                        csv_constructor,
                        f"constructor_results_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-constructor'
                    )

                # Add Constructor Standings section
                if st.session_state.selected_sections.get('Constructor Standings', False):
                    st.subheader("Constructor Standings")
                    constructor_standings = get_constructor_standings(year, selected_round)
                    st.dataframe(constructor_standings)
                    
                    # Add download button for constructor standings
                    csv_standings = constructor_standings.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Constructor Standings",
                        csv_standings,
                        f"constructor_standings_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-constructor-standings'
                    )

                # Add Constructors Data section
                if st.session_state.selected_sections.get('Constructors Data', False):
                    st.subheader("Constructors/Teams")
                    constructors = get_constructors_data(year, selected_round)
                    st.dataframe(constructors)
                    
                    # Add download button for constructors data
                    csv_constructors = constructors.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Constructors Data",
                        csv_constructors,
                        f"constructors_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-constructors'
                    )

                # Add Drivers Data section
                if st.session_state.selected_sections.get('Drivers Data', False):
                    st.subheader("Drivers Information")
                    drivers = get_drivers_data(year, selected_round)
                    st.dataframe(drivers)
                    
                    # Add download button for drivers data
                    csv_drivers = drivers.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Drivers Data",
                        csv_drivers,
                        f"drivers_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-drivers'
                    )

                # Add Lap Times section
                if st.session_state.selected_sections.get('Lap Times', False):
                    st.subheader("Lap Times")
                    lap_times = get_lap_times(year, selected_round)
                    st.dataframe(lap_times)
                    
                    # Add download button for lap times data
                    csv_lap_times = lap_times.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Lap Times Data",
                        csv_lap_times,
                        f"lap_times_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-lap-times'
                    )

                # Add Pit Stops Data section
                if st.session_state.selected_sections.get('Pit Stops Data', False):
                    st.subheader("Pit Stops")
                    pit_stops = get_pit_stops(year, selected_round)
                    
                    if pit_stops is not None:
                        st.dataframe(pit_stops)
                        # Add download button for pit stops data
                        csv_pit_stops = pit_stops.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download Pit Stops Data",
                            csv_pit_stops,
                            f"pit_stops_{year}_round_{selected_round}.csv",
                            "text/csv",
                            key='download-pit-stops'
                        )
                    else:
                        st.info("No pit stops data available for this race")

                # Add Qualifying Results section
                if st.session_state.selected_sections.get('Qualifying Results', False):
                    st.subheader("Qualifying Results")
                    qualifying = get_qualifying_results(year, selected_round)
                    st.dataframe(qualifying)
                    
                    # Add download button for qualifying results
                    csv_qualifying = qualifying.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Qualifying Results",
                        csv_qualifying,
                        f"qualifying_results_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-qualifying'
                    )

                # Add Races Data section
                if st.session_state.selected_sections.get('Races Data', False):
                    st.subheader("Race Schedule Information")
                    races = get_races_data(year)
                    st.dataframe(races)
                    
                    # Add download button for races data
                    csv_races = races.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Races Data",
                        csv_races,
                        f"races_data_{year}.csv",
                        "text/csv",
                        key='download-races'
                    )

                # Add Season Data section
                if st.session_state.selected_sections.get('Season Data', False):
                    st.subheader("Season Schedule")
                    season = get_season_data(year)
                    st.dataframe(season)
                    
                    # Add download button for season data
                    csv_season = season.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Season Data",
                        csv_season,
                        f"season_data_{year}.csv",
                        "text/csv",
                        key='download-season'
                    )

                # Add Sprint Race Results section
                if st.session_state.selected_sections.get('Sprint Race Results', False):
                    st.subheader("Sprint Race Results")
                    sprint_results = get_sprint_results(year, selected_round)
                    
                    if sprint_results is not None:
                        st.dataframe(sprint_results)
                        # Add download button for sprint results
                        csv_sprint = sprint_results.to_csv(index=False).encode('utf-8')
                        st.download_button(
                            "Download Sprint Race Results",
                            csv_sprint,
                            f"sprint_results_{year}_round_{selected_round}.csv",
                            "text/csv",
                            key='download-sprint'
                        )
                    else:
                        st.info("No sprint race data available for this event")

                # Only fetch selected data sections
                if st.session_state.selected_sections.get('Race Results', False):
                    st.subheader("Race Results")
                    results = load_race_results(year, selected_round)
                    st.dataframe(results)
                    
                    # Add download button for complete race results
                    csv_results = results.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Complete Race Results",
                        csv_results,
                        f"race_results_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-results'
                    )
                
                if st.session_state.selected_sections.get('Driver Standings', False):
                    st.subheader("Driver Standings")
                    standings_df = get_driver_standings(year, selected_round)
                    st.dataframe(standings_df)
                    # Add download button for standings
                    csv_standings = standings_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Driver Standings",
                        csv_standings,
                        f"driver_standings_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-driver-standings'
                    )
                
                # Add Status Data section
                if st.session_state.selected_sections.get('Status Data (Race Completion Status)', False):
                    st.subheader("Race Completion Status")
                    status = get_status_data(year, selected_round)
                    st.dataframe(status)
                    
                    # Add download button for status data
                    csv_status = status.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        "Download Status Data",
                        csv_status,
                        f"race_status_{year}_round_{selected_round}.csv",
                        "text/csv",
                        key='download-status'
                    )
                
            except Exception as e:
                st.error(f"Error loading race data: {str(e)}")

if __name__ == '__main__':
    main()
