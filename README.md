# F1RDF - Formula 1 Race Data Fetcher 🏎️

A Streamlit application that provides comprehensive Formula 1 racing data from 1950 to present.

## Features

- Historical race data from 1950 to present
- Interactive data selection interface
- 14 different data categories including:
  - Race Results
  - Driver & Constructor Standings
  - Lap Times
  - Pit Stops
  - Qualifying Results
  - Sprint Race Results
  - Circuit Information
  - And more...
- CSV export functionality for all data tables
- Beautiful F1-themed UI

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd "Fast F1 App 🚗"
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run ui.py
```

## How to Use

1. Select a year from the sidebar dropdown (1950-present)
2. Choose a Grand Prix from the available races
3. Select the data sections you want to view
4. Click "Fetch Selected Data" to load the information
5. Download any table as CSV using the download buttons below each section

## Data Categories

- **Circuits Data**: Track information and details
- **Constructor Results & Standings**: Team performance data
- **Drivers Data & Standings**: Driver information and championship positions
- **Lap Times**: Detailed lap-by-lap timing
- **Pit Stops**: Pit stop timing and statistics
- **Qualifying Results**: Grid position and qualifying times
- **Race Results**: Final race classifications
- **Sprint Results**: Sprint race outcomes (where applicable)
- **Status Data**: Race completion status for each driver

## Requirements

- Python 3.7+
- Streamlit
- Pandas
- Matplotlib

