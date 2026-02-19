# F1RDF - Formula 1 Race Data Fetcher 🏎️

A Streamlit application that provides comprehensive Formula 1 racing data from 1950 to present.

![f1drf](https://github.com/user-attachments/assets/febeda48-a2b2-4803-bb3c-7994aafbf189)
<img width="1919" height="971" alt="image" src="https://github.com/user-attachments/assets/d0dd6eeb-54d3-454d-9ba6-fddcc9b02d5e" />



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
- fastf1
- Streamlit
- Pandas
- Matplotlib



