import streamlit as st
import pandas as pd
import plotly.express as px
import re
from .sec_details import displayDetails

def change_state():
    st.session_state.show_details = True
    return

def renderPortfolio(portfolio_data):

    if "show_details" not in st.session_state:
        st.session_state.show_details = False


    # Extract portfolio data into a DataFrame
    portfolio_df = pd.DataFrame(
        [
            [ticker] + details
            for item in portfolio_data["portfolio"]
            for ticker, details in item.items()
        ],
        columns=["Ticker", "Category", "Allocation", "Dollar Amount", "Rationale"]
    )

    st.session_state.portfolio_df = portfolio_df

    # Set up Streamlit layout
    st.title("Portfolio View")

    # First div: Chart and table
    st.subheader("Portfolio Allocation and Details")
    st.write(f"{portfolio_data['date']}")
    col1, col2 = st.columns([5, 5])

    # Doughnut chart
    with col1:
        st.write("### Asset Allocation")
        fig = px.pie(
            portfolio_df,
            names="Ticker",
            values="Allocation",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # Table with clickable rows
    with col2:
        st.write("### Securities Overview")
        for _, row in portfolio_df.iterrows():
            with st.expander(f"{row['Ticker']} ({row['Category']}) - {row['Allocation']*100:.0f}%", expanded="print_view" in st.session_state):
                st.write(f"**Ticker:** {row['Ticker']}")
                st.write(f"**Category:** {row['Category']}")
                st.write(f"**Allocation:** {row['Allocation']*100:.0f}%")
                st.write(f"**Dollar Amount:** ${row['Dollar Amount']}")
                st.write("**Rationale:**")
                st.write(row["Rationale"])
    # Second div: Portfolio rationale
    st.subheader("Portfolio Rationale")
    st.write(re.sub(r"([_*#[\]()$\\`])", r"\\\1", portfolio_data["port_rational"]))

    

    # Button to toggle detailed views
    st.button("Generate Detailed Securities Views", on_click=change_state)
        

    # Detailed securities view (renders below the portfolio overview)
    if st.session_state.show_details:
        displayDetails(st.session_state.portfolio_df)



    # Third div: Warnings and disclaimers
    st.subheader("Warnings and Disclaimers")
    st.markdown(
        f"<i>{portfolio_data['warnings']}</i>",
        unsafe_allow_html=True
    )