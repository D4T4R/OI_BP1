import sys
sys.path.append("/usr/local/lib/python3.10/dist-packages")
sys.path.append("/local/lib/python3.10/site-packages")
import requests
import plotly.graph_objects as go

# Placeholder variables
selected_expiry_date = "28-Dec-2023"  # Replace with your desired expiry date
lot_size = 50  # Replace with your desired lot size

# The general URL for fetching NIFTY options data
url = "https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.nseindia.com/"
}

# Make the HTTP request to the NSE API
response = requests.get(url, headers=headers)

# Initialize lists to store the parsed data
strike_prices = []
ce_open_interests = []
pe_open_interests = []

if response.status_code == 200:
    data = response.json()  # Parse the JSON data from the response
    # Filter the required data for the specific expiry date
    for record in data['records']['data']:
        if record['expiryDate'] == selected_expiry_date:
            strike_prices.append(record['strikePrice'])
            # Check if CE and PE data is available and multiply by lot size
            if 'CE' in record:
                ce_open_interests.append((record['CE']['openInterest'] * lot_size) / 1e6)  # Convert to millions
            else:
                ce_open_interests.append(0)
            if 'PE' in record:
                pe_open_interests.append((record['PE']['openInterest'] * lot_size) / 1e6)  # Convert to millions
            else:
                pe_open_interests.append(0)
else:
    print("Failed to retrieve data:", response.status_code)

# Creating traces for the Plotly graph
trace1 = go.Bar(
    x=strike_prices,
    y=ce_open_interests,
    name='CE Open Interest'
)
trace2 = go.Bar(
    x=strike_prices,
    y=pe_open_interests,
    name='PE Open Interest'
)

# Creating the layout for the Plotly graph with increased size
layout = go.Layout(
    title=f'NIFTY Call and Put Open Interest for {selected_expiry_date} (Lot Size: {lot_size})',
    xaxis=dict(
        title='Strike Price',
        tickmode='array',
        tickvals=strike_prices[::5]  # Show every 5th strike price for readability
    ),
    yaxis=dict(
        title='Open Interest (in millions)'
    ),
    barmode='group',
    width=1200,  # Width of the figure in pixels
    height=800   # Height of the figure in pixels
)

# Creating the figure with the data and layout
fig = go.Figure(data=[trace1, trace2], layout=layout)

# Display the plot
fig.show()
