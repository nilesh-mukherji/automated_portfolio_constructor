import streamlit as st
import json
import re
from hidden_pages.portfolio_render import renderPortfolio
from hidden_pages.gemeni_call import callGemini

import os

RECS = """
        ```json 
        {
        "portfolio": [
            {"VOO": ["Equity", 0.60, 12000, "Vanguard S&P 500 ETF: A low-cost, diversified core holding tracking the S&P 500. Its historical beta is approximately 1, representing market-like volatility. While alpha is expected to be close to zero over the long run for a broad market index, it provides solid, stable returns over time, suitable for a long-term growth portfolio."]},
            {"VUG": ["Equity", 0.20, 4000, "Vanguard Growth ETF: Targets high-growth U.S. companies, offering higher potential returns but with increased volatility. Historically, growth stocks have exhibited betas greater than 1 and potentially positive alphas, aligning with the investor's growth objective and risk tolerance.  However, remember past performance is not indicative of future results."]},
            {"QQQ": ["Equity", 0.10, 2000, "Invesco QQQ Trust: Tracks the Nasdaq-100 index, heavily weighted towards technology companies. This adds exposure to a specific sector with historically high growth potential.  Be mindful that technology is subject to rapid innovation and disruption, so higher beta and potential alpha come with increased risk."]},
            {"BND": ["Fixed Income", 0.10, 2000, "Vanguard Total Bond Market ETF:  Provides diversification and a stable income component. Bonds generally have low betas (close to 0 or even negative) and provide ballast against equity market volatility.  While alpha is typically low, their role is to mitigate portfolio risk, especially during market downturns."]}
        ],
        "port_rational": "This portfolio emphasizes growth by allocating 90% to equities and 10% to fixed income, reflecting the investor's long-term horizon, growth objective, and moderately high risk tolerance.  The equity portion blends broad market exposure with growth-focused ETFs to target higher returns. The small allocation to fixed income provides some stability and diversification.  The initial allocation uses the available $20,000. Future contributions should maintain the target allocation percentages. As the portfolio grows, consider diversifying further into international equities or other asset classes.",
        "warnings": "This is not financial advice. Past performance is not indicative of future results. All investment decisions should be made after careful research and consultation with a qualified financial advisor. The allocation percentages are suggestions and should be adjusted based on individual circumstances, risk tolerance, and investment goals.  Beta and alpha values are historical and can change over time.  Market conditions and economic factors significantly influence investment returns. Consider the impact of inflation, interest rate changes, and geopolitical events.  Rebalance the portfolio periodically to maintain the target asset allocation.",
        "date": "2024-07-15"
        }
        ```
        """


# Function to interact with the Gemini API
def get_recommendations(profile):
    return (
            "Given the following profile, suggest a Python-formatted list of stocks (tickers) "
            "that the user should consider investing in. Please reference historical beta and "
            "historical alpha (according to the CAPM model), as well as a suitable equities and "
            f"fixed income split: \"{profile}\"." +  ' It is essential to use this JSON format: {"portfolio":[{"ticker_value": ["security_type", "Allocation % as float", "Allocation $ as int", "Rational for security"]}], "port_rational": "Rational for portfolio construction", "warnings": "Warnings and disclaimers", "date": "current date in format YYYY-MM-DD"}'
            "Please Ensure the format of the return is JSON compliant, meaning no characters that JSON cannot Accept"
        )


def add_profile(profile_input):
    if profile_input.strip():
        with st.spinner("Fetching recommendations..."):
            if GENERATE_DATA:
                recommendations = callGemini(get_recommendations(profile_input))
            else:
                recommendations = RECS

            json_match = re.search(r'```json\s*(\{.*?\})\s*```', recommendations, re.DOTALL)

            extracted_json = json_match.group(1) if json_match else None

            if not extracted_json:
                st.write("JSON Not in response")
            else:
                st.session_state.extracted_json = extracted_json
    else:
        st.warning("Please enter a valid investment profile.")

def build_prompt_from_form(name, age, location, investable_assets, risk_tolerance, investment_goal):
    return f"{name} is {age} years old, and is living in {location}. They have {investable_assets} dollars in investable assets, "\
        f"and a {risk_tolerance} risk tolerance. Their investment goals include: {investment_goal}"

def build_profile_form():
    col1, col2 = st.columns(2)
    
    with col1:
        # Input fields for personal information
        st.subheader("Personal Information")
        name = st.text_input("Full Name", placeholder="Enter your full name")
        age = st.number_input("Age", min_value=0, max_value=120, step=1, help="Enter the age in years")
        location = st.text_input("Location", placeholder="Enter your city or country")
    
    with col2:
        # Input fields for financial profile
        st.subheader("Financial Profile")
        investable_assets = st.number_input(
            "Investable Assets ($)", 
            min_value=0, 
            step=1000, 
            help="Enter the total investable assets in dollars"
        )
        risk_tolerance = st.select_slider(
            "Risk Tolerance",
            options=["Low", "Moderate", "High"],
            help="Choose your investment risk tolerance level"
        )
        investment_goal = st.text_area(
            "Investment Goal",
            placeholder="Describe your primary investment goal (e.g., retirement, buying a house)"
        )

        def gen_prompt(name, age, location, investable_assets, risk_tolerance, investment_goal): st.session_state.default_prompt =  build_prompt_from_form(name, age, location, investable_assets, risk_tolerance, investment_goal)

        st.button("Let's make a prompt!", on_click=lambda: gen_prompt(name, age, location, investable_assets, risk_tolerance, investment_goal))

        return (name, age, location, investable_assets, risk_tolerance, investment_goal)


def main():
    if "extracted_json" not in st.session_state:
        st.session_state.default_prompt = "e.g., 24 year old aiming to generate a growth-driven portfolio..."
        # Streamlit app
        st.title("Investment Portfolio Recommender")

        # Input for the user profile
        profile_input = st.text_area("Enter your investment profile", 
                                    value=st.session_state.default_prompt)

        # Button to generate recommendations
        st.button("Get Recommendations", on_click=lambda: add_profile(profile_input))

        # Form for prompt building
        form_on = st.toggle("Need some help?", value=False)

        if form_on:
            build_profile_form()


        

    else:
            try:
                renderPortfolio(json.loads(st.session_state.extracted_json))
            except:
                st.subheader("Whoops!")
                print(st.session_state.extracted_json)
                st.button("Reload")
            # Initialize session state
            if "current_card" not in st.session_state:
                st.session_state.current_card = 0

            def new_prof(): 
                try:
                    del st.session_state.extracted_json
                except:
                    pass
                try:
                    del st.session_state.portfolio
                except:
                    pass
                try:
                    del st.session_state.show_details
                except:
                    pass

            st.button("Analyze a new Profile", on_click=new_prof)
            
            def print_view(): 
                if "print_view" not in st.session_state:
                    st.session_state.print_view = True
                else:
                    del st.session_state.print_view
            st.toggle("PDF Format", on_change=print_view, value="print_view" in st.session_state)
                

if __name__ == "__main__":
    # API_KEY = os.getenv("API_KEY")
    GENERATE_DATA = os.getenv("GENERATE_DATA") == '1'

    # Set up your Gemini API key
    # genai.configure(api_key=API_KEY)

    st.html("""
        <style>
            .stMainBlockContainer {
                max-width:70rem;
            }
            
            @media print {
                .stButton, .stCheckbox {
                    display: none;
                }
                .stToggle {
                    display: none;
                }
            }
        </style>
        """
    )

    main()

