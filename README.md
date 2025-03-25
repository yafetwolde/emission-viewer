# Emission Data Viewer

A web-based dashboard for viewing vessel emission data. This application displays detailed emission and operational data for vessels, including CO2 emissions, fuel consumption, and operational metrics.

## Features

- Real-time data fetching from the BWES Global API
- Interactive filters:
  - Date range selection
  - Vessel name search
  - Vessel class filtering
- Detailed vessel information display:
  - CO2 emissions
  - Fuel consumption metrics
  - Operational statistics
  - Distance and time utilization
- Responsive design
- Clean, modern UI

## Setup

1. Clone the repository:
```bash
git clone https://github.com/japhettcw/emission-viewer.git
```

2. Navigate to the project directory:
```bash
cd emission-viewer
```

3. Start the Python server:
```bash
python server.py
```

4. Open your web browser and visit:
```
http://localhost:8000
```

## Requirements

- Python 3.7+
- Web browser with JavaScript enabled

## API Documentation

The application uses the BWES Global API for fetching emission data. Required parameters:
- api_key: Your API authentication key
- start_date: Start date for data range (YYYY-MM-DD)
- end_date: End date for data range (YYYY-MM-DD)

## License

MIT License 