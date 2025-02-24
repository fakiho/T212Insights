# T212 insights OpenWebUI Tool

This is an OpenWebUI tool for interacting with the [Trading 212 API](https://t212public-api-docs.redoc.ly). It allows users to fetch account details, check open positions, review past orders, analyze market data, and suggest potential trading moves.

## Features
- Retrieve account balance and cash details
- Fetch open positions and past orders
- Perform basic trading analysis (the performance depends on the Model you are using)
- Fetch latest market news (if supported)
- Suggest possible trade strategies based on data

## Installation

### Prerequisites
- Ensure you have [OpenWebUI](https://docs.openwebui.com) installed and running
- Python 3.8+ installed

### Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/fakiho/T212Insights.git
   cd T212Insights
   ```
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your OpenWebUI tool:
   - Register the tool in OpenWebUI following [this guide](https://docs.openwebui.com/features/plugin/tools/)
   - Provide API credentials for Trading 212

## Usage
Once installed, you can use the tool within OpenWebUI to retrieve trading information. Example usage:

- **Get account cash details**:
  ```json
  {
    "prompt": "what is the available cash in my account"
  }
  ```
- **Fetch open positions**:
  ```json
  {
    "prompt": "get all open position in my portfolio"
  }
  ```
- **Analyze past orders**:
  ```json
  {
    "prompt": "analyze my past orders"
  }
  ```

## Configuration
Update the tool's configuration file with your Trading 212 API key and preferences. Example:
```json
{
  "api_key": "your_api_key_here",
  "base_url": "https://api.trading212.com"
}
```

## Contribution
Feel free to submit pull requests and report issues.
