from typing import Type, Dict, Any, Union
import time 
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import yfinance as yf
import logging

class MyToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    ticker: str = Field(..., description="Ticker symbol of the company to fetch financial ratios for.")


class Getfinancialratios(BaseTool):
    name: str = "Getfinancialratios"
    description: str = "Get key financial ratios for a company"
    args_schema: Type[BaseModel] = MyToolInput

    def _run(self, ticker: str) -> Union[Dict[str, Any], str]:
        """Get key financial ratios for a company with retries for all keys."""
        if not ticker:
            return "Ticker symbol is required"

        keys_to_fetch = {
            'P/E Ratio': 'forwardPE',
            'P/B Ratio': 'priceToBook',
            'Debt to Equity': 'debtToEquity',
            'Current Ratio': 'currentRatio',
            'Profit Margin': 'profitMargins',
            'ROE': 'returnOnEquity',
        }

        try:
            stock = yf.Ticker(ticker)
            info = None

            # Retry logic for all required keys
            for attempt in range(3):
                info = stock.info
                if all(info.get(key) is not None for key in keys_to_fetch.values()):
                    break  # Exit if all keys are available
                logging.warning(
                    f"Retry {attempt + 1}: Some keys are missing for ticker {ticker}. Retrying..."
                )
                time.sleep(1)
            
            # Final extraction of values
            return {
                label: info.get(key, "N/A")
                for label, key in keys_to_fetch.items()
            }
        except KeyError as ke:
            logging.error(f"KeyError for ticker {ticker}: {str(ke)}")
            return "Missing key in the fetched data"
        except Exception as e:
            logging.error(f"Error fetching data for ticker {ticker}: {str(e)}")
            return "Error fetching financial ratios"


