import pandas as pd
import yfinance as yf
from .gemeni_call import callGemini
import streamlit as st


def generate_descriptions(df):
    portfolio_data = []
    df = df[["Ticker", "Category"]].copy()
    df.loc[: ,"Description"] = [""]*len(df)
    historical_vals = {}
    for i, row in df.iterrows():
        prompt = f"Please give me 5 to 7 paragraphs of thorough analysis about the security with ticker {row.Ticker}, a/an {row.Category} product. "\
        "Please ensure this analysis to to the quality that would be required for an investment decision."
        df.loc[i, "Description"] = callGemini(prompt=prompt)
        historical_vals[i] = get_historical_prices(row.Ticker)

    print(historical_vals)

    for i, row in df.iterrows():
        portfolio_data.append({
            "Ticker": row.Ticker,
            "Category": row.Category,
            "Description": row.Description,
            "Historical Data": [j[1] for j in historical_vals[i]],
            "Time": [j[0] for j in historical_vals[i]]
        })

        
    return portfolio_data


def get_historical_prices(ticker: str):
    """
    Retrieves 3 years of historical stock price data in 1-month increments for a given ticker.

    Parameters:
        ticker (str): The stock ticker symbol (e.g., "AAPL").

    Returns:
        list: A list of tuples in the format [(date, close), ...].
    """
    try:
        # Get today's date and calculate the start date (3 years ago)
        end_date = pd.Timestamp.today()
        start_date = end_date - pd.DateOffset(years=3)
        
        # Download the data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date, interval="1mo")

        st.table(data)
        
        if data.empty:
            print(f"No data found for ticker: {ticker}")
            return []

        # Extract the required columns and convert to a list of tuples
        result = [(row.name.strftime('%Y-%m-%d'), row['Close']) for _, row in data.iterrows()]
        
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

if __name__ == "__main__":
    data = pd.read_csv("test.csv")
    print(generate_descriptions(data))
    print("-"*10)