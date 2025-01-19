
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from streamlit_card import card
from investmentcrew.crew import Investmentcrew

# Create Investment Dashboard
def create_investment_dashboard(data):
    st.title(f"{data['company_name']} ({data['stock_ticker']}) Analysis")
    
    # Short-term and Long-term Analysis Cards
    col1, col2 = st.columns(2)
    
    with col1:
        card(
            title="Short-Term Outlook",
            text=f"""
            Action: {data['short_term_decision']['investment_action']}
            
            Confidence: {data['short_term_decision']['confidence_score']}%
            
            {data['short_term_decision']['analysis']}
            """,
            styles={
                "card": {
                    "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                    "height": "300px" # <- if you want to set the card height to 300px
                    
                    }
                }
        )
    
    with col2:
        card(
            title="Long-Term Outlook",
            text=f"""
            Action: {data['long_term_decision']['investment_action']}\n
            Confidence: {data['long_term_decision']['confidence_score']}%\n
            {data['long_term_decision']['analysis']}\n
            """,
            styles={
                "card": {
                    "width": "100%", # <- make the card use the width of its container, note that it will not resize the height of the card automatically
                    "height": "300px" # <- if you want to set the card height to 300px
                    
                    }
                }
        )
    
    # Summary and Conclusion
    st.header("Investment Summary")
    st.info(data['summary'])
    
    st.header("Conclusion")
    st.markdown(data['conclusion'])

def main():
    st.set_page_config(layout="wide")
    st.title("ProfitPilot AI")
    st.write("ProfitPilot AI is an AI Agent that helps you analyze stocks for both short-term and long-term investments.")
    
    # Sidebar
    with st.sidebar:
        ticker = st.text_input("Enter Stock Ticker:", "TSLA")
        analyze_button = st.button("Analyze Stock")

    if analyze_button:
        try:
            with st.spinner("Analyzing..."):
                crew = Investmentcrew()
                raw_results = crew.crew().kickoff(inputs={'ticker': ticker})
                
                # Convert raw results to structured data
                investment_data = {
                    'company_name': raw_results['company_name'],
                    'stock_ticker': raw_results['stock_ticker'],
                    'short_term_decision': raw_results['short_term_decision'],
                    'long_term_decision': raw_results['long_term_decision'],
                    'summary': raw_results['summary'],
                    'conclusion': raw_results['conclusion']
                }
                
                create_investment_dashboard(investment_data)
                
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")

if __name__ == "__main__":
    main()
