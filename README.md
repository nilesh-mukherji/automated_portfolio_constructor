# **Automated Portfolio Constructor**

The Automated Portfolio Constructor is a Streamlit-based application designed to help users build and analyze investment portfolios dynamically. It provides detailed views of portfolio allocation, individual securities, and performance metrics, with the ability to export session-specific data to PDF.

## **Features**
- **Dynamic Portfolio Visualization**:
  - Interactive charts (e.g., pie charts for allocation).
  - Detailed security analysis with historical performance and rationale.
- **Customizable Reports**:
  - Generate tailored investment summaries for specific portfolios.
  - Export reports and app state to PDF format.
- **Interactive User Experience**:
  - Expandable sections for securities with detailed descriptions.
  - Navigation across multiple cards for securities analysis.
- **Responsive Design**:
  - Optimized layout for charts, tables, and user inputs.

## **Installation**

1. **Clone the Repository**
   ```bash
   git clone https://github.com/nilesh-mukherji/automated_portfolio_constructor.git
   cd automated_portfolio_constructor
   ```
  
2. **Install Dependencies**
    Run the following command to install all required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## **Run the Application**

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
    ```
2. Open your browser and navigate to Open your browser and navigate to: http://localhost:8501

## **Usage**

### **Portfolio Overview**
- Launch the app and upload your portfolio data in JSON format.
- View portfolio allocation as an interactive pie chart.
- Expand individual securities in the table for detailed insights.

### **Detailed Security View**
- Navigate through a card-based view showing:
  - Historical performance charts.
  - In-depth descriptions of individual securities.

### **Export Options**
- Use the "Generate PDF" button to export the portfolio analysis as a PDF.



