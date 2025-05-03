import fastf1
import pandas as pd
import os
from pathlib import Path

# Setup cache directory
try:
    CACHE_DIR = Path("D:/umer/Fast F1 App 🚗/cache")
    # Create cache directory if it doesn't exist
    if not CACHE_DIR.exists():
        os.makedirs(CACHE_DIR)
    
    # Enable FastF1 cache
    fastf1.Cache.enable_cache(CACHE_DIR)
except Exception as e:
    print(f"Error setting up cache: {str(e)}")

def load_schedule(year):
    schedule = fastf1.get_event_schedule(year)
    return schedule

def load_race_results(year, round_number):
    """Get complete race results for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    return session.results

def get_driver_standings(year, round_number):
    """Get driver standings for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get results with specified columns and sort by position
    standings = session.results[['DriverId', 'Abbreviation', 'FullName', 'TeamName', 'Points', 'Position']]
    standings = standings.sort_values('Position')
    standings.columns = ['Driver ID', 'Abbreviation', 'Full Name', 'Team', 'Points', 'Position']
    return standings

def get_circuit_info(year, round_number):
    """Get circuit information for a specific race"""
    schedule = fastf1.get_event_schedule(year)
    circuit_info = schedule[schedule['RoundNumber'] == round_number].iloc[0]
    
    # Get all sessions info
    sessions = {
        'Session1': {
            'name': circuit_info['Session1'],
            'date': circuit_info['Session1Date'],
            'utc': circuit_info['Session1DateUtc']
        },
        'Session2': {
            'name': circuit_info['Session2'],
            'date': circuit_info['Session2Date'],
            'utc': circuit_info['Session2DateUtc']
        },
        'Session3': {
            'name': circuit_info['Session3'],
            'date': circuit_info['Session3Date'],
            'utc': circuit_info['Session3DateUtc']
        },
        'Session4': {
            'name': circuit_info['Session4'],
            'date': circuit_info['Session4Date'],
            'utc': circuit_info['Session4DateUtc']
        },
        'Session5': {
            'name': circuit_info['Session5'],
            'date': circuit_info['Session5Date'],
            'utc': circuit_info['Session5DateUtc']
        }
    }
    
    return {
        'name': circuit_info['Location'],
        'country': circuit_info['Country'],
        'event': circuit_info['OfficialEventName'],
        'format': circuit_info['EventFormat'],
        'event_date': circuit_info['EventDate'],
        'sessions': sessions
    }

def get_constructor_results(year, round_number):
    """Get constructor results for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get constructor results with specified columns
    constructor_results = session.results[['DriverId', 'TeamName', 'FullName', 'Position', 'Points', 'Status', 'Time']]
    constructor_results.columns = ['Driver ID', 'Team', 'Full Name', 'Position', 'Points', 'Status', 'Time']
    return constructor_results

def get_constructor_standings(year, round_number):
    """Get constructor standings for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get constructor standings with specified columns
    standings = session.results[['DriverId', 'TeamName', 'FullName', 'Position', 'Points', 'Status', 'Time']]
    standings = standings.sort_values('Points', ascending=False)  # Sort by points
    standings.columns = ['Driver ID', 'Team', 'Full Name', 'Position', 'Points', 'Status', 'Time']
    return standings

def get_constructors_data(year, round_number):
    """Get unique constructors/teams data for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get unique constructors with specified column
    constructors = session.results[['TeamName']].drop_duplicates()
    constructors.columns = ['Team Name']
    return constructors

def get_drivers_data(year, round_number):
    """Get drivers data for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get drivers data with specified columns
    drivers = session.results[[
        'DriverNumber', 'DriverId', 'Abbreviation',
        'FirstName', 'LastName', 'FullName', 'TeamName'
    ]].drop_duplicates()
    
    drivers.columns = [
        'Number', 'Driver ID', 'Abbreviation',
        'First Name', 'Last Name', 'Full Name', 'Team'
    ]
    return drivers

def get_lap_times(year, round_number):
    """Get lap times data with sector times for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get lap times with specified columns
    lap_times = session.laps[[
        'Driver', 'LapNumber', 'LapTime', 'Position',
        'Time', 'Sector1Time', 'Sector2Time', 'Sector3Time'
    ]]
    
    lap_times.columns = [
        'Driver', 'Lap Number', 'Lap Time', 'Position',
        'Time', 'Sector 1', 'Sector 2', 'Sector 3'
    ]
    return lap_times

def get_pit_stops(year, round_number):
    """Get pit stops data for a specific race"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get pit stops data with specified columns
    laps = session.laps
    pit_stops = laps[laps['PitOutTime'].notna()][
        ['Driver', 'LapNumber', 'PitOutTime', 'PitInTime']
    ].copy()
    
    # Return None if no pit stops data available
    if pit_stops.empty:
        return None
        
    pit_stops.columns = ['Driver', 'Lap Number', 'Pit Out Time', 'Pit In Time']
    return pit_stops

def get_qualifying_results(year, round_number):
    """Get qualifying results for a specific race"""
    session = fastf1.get_session(year, round_number, 'Q')
    session.load()
    
    # Get qualifying results with specified columns
    qualifying = session.results[[
        'Abbreviation', 'DriverId', 'FullName', 'TeamName',
        'Q1', 'Q2', 'Q3', 'Position'
    ]]
    
    qualifying.columns = [
        'Abbreviation', 'Driver ID', 'Full Name', 'Team',
        'Q1 Time', 'Q2 Time', 'Q3 Time', 'Position'
    ]
    return qualifying

def get_races_data(year):
    """Get races data from event schedule"""
    events = fastf1.get_event_schedule(year)
    
    # Get races data with specified columns
    races = events[[
        'RoundNumber', 'EventName', 'OfficialEventName',
        'Location', 'Country', 'Session1Date', 'Session5Date'
    ]]
    
    races.columns = [
        'Round', 'Event Name', 'Official Event Name',
        'Location', 'Country', 'First Session', 'Last Session'
    ]
    return races

def get_season_data(year):
    """Get season schedule data"""
    events = fastf1.get_event_schedule(year)
    
    # Get season data with specified columns
    season = events[[
        'RoundNumber', 'EventName', 'Location', 'Country',
        'Session1Date', 'Session5Date'
    ]]
    
    season.columns = [
        'Round', 'Event Name', 'Location', 'Country',
        'First Session', 'Last Session'
    ]
    return season

def get_sprint_results(year, round_number):
    """Get complete sprint race results"""
    try:
        session = fastf1.get_session(year, round_number, 'S')
        session.load()
        return session.results
    except:
        return None  # Return None if no sprint race data available

def get_status_data(year, round_number):
    """Get race completion status data"""
    session = fastf1.get_session(year, round_number, 'R')
    session.load()
    
    # Get status data with specified columns
    status = session.results[['Abbreviation', 'FullName', 'Status']]
    status.columns = ['Abbreviation', 'Full Name', 'Status']
    return status
