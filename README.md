# Crefia Credit Card Issuer Data Visualization

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/f75f3e07-cfe5-4788-aee1-976a57d2dfce" />
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://crefia-data.streamlit.app)

## Features

- **Interactive Dashboard**: Visualize and compare key metrics (total members, active users, new members, cancellations) for major credit card issuers.
- **Time Series Analysis**: Select custom date ranges to analyze trends over time.
- **Data Table Views**: View underlying data in pivoted tables for each metric.
- **Multi-Card Comparison**: Easily compare across Shinhan, Hyundai, Woori, Samsung, Lotte, Hana, and KB Kookmin cards.
- **Custom Color Coding**: Each issuer is color-coded for clarity in all visualizations.

## Data Pipeline

1. **Raw Data Conversion** (`0_fetch_data.py`):
   - Converts monthly `.xls` files from the `data/` directory into standardized CSVs using column labels from `crefia_label.csv`.
   - Outputs to the `csv/` directory.

2. **Database Aggregation** (`1_to_sqlite3.py`):
   - Merges all monthly CSVs into a single SQLite database (`master.db`) for efficient querying and analysis.

3. **Preprocessing & Analysis** (`2_data_preprocessing.py`, `3_data_analysis.py`):
   - Loads and preprocesses the master data for further analysis and visualization.

4. **Visualization** (`4_visualize_data.py`):
   - Launches a Streamlit dashboard for interactive exploration of the data.

## Getting Started

### Prerequisites

- Python 3.7+
- The following Python packages (see `requirements.txt`):
  - streamlit
  - pandas
  - plotly
  - seaborn
  - matplotlib

### Installation

1. **Clone the repository** and navigate to the project directory.
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Prepare the data**:
   - Place raw monthly `.xls` files in the `data/` directory.
   - Ensure `crefia_label.csv` is in the project root.

4. **Run the data pipeline**:
   ```bash
   python 0_fetch_data.py
   python 1_to_sqlite3.py
   ```

5. **Launch the dashboard**:
   ```bash
   streamlit run 4_visualize_data.py
   ```

## Usage

- Use the dashboard to select time periods and metrics.
- Compare trends across different credit card issuers.
- Download or inspect the underlying data tables as needed.

## Data Sources

- **Crefia (여신금융협회)**: Official monthly statistics on credit card usage and membership.

## License

This project is licensed under the MIT License. 
