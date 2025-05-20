# Real-Time Portfolio Analysis Tool

A Streamlit-based dashboard for real-time stock market analysis and forecasting using the Alpaca API.

## Features

- Real-time stock data visualization
- Multiple stock/ETF tracking
- Simple moving average forecasting
- Interactive charts and graphs
- Customizable time periods

## Prerequisites

- Python 3.9 or higher
- Alpaca API credentials (paper trading account)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Real-Time-Portfolio-Analysis-Tool.git
cd Real-Time-Portfolio-Analysis-Tool
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your Alpaca API credentials:
   - Create a `.streamlit/secrets.toml` file in the project root
   - Add your API credentials:
```toml
ALPACA_API_KEY = "your_api_key_here"
ALPACA_SECRET_KEY = "your_secret_key_here"
```

## Usage

Run the Streamlit app:
```bash
cd live_portfolio_dashboard
streamlit run streamlit_app.py
```

The dashboard will be available at `http://localhost:8501`

## Configuration

- Modify the default tickers in `streamlit_app.py`
- Adjust the time period for data fetching
- Customize the moving average window size

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
