import logging
import pandas as pd
from flask import Flask, render_template, request
from models.forecasting_models import ForecastingModel
from models.nlp_models import DocumentProcessor

# Configure logging
logging.basicConfig(
    filename='logs/application.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)

class BudgetForecastingApp:
    def __init__(self):
        self.model = None
        self.load_data_and_train_model()
        self.setup_routes()

    def load_data_and_train_model(self):
        try:
            logging.info("Loading data...")
            budget_data = pd.read_csv('data/historical_budget_data.csv')
            economic_data = pd.read_csv('data/economic_indicators.csv')
            self.model = ForecastingModel.train(budget_data, economic_data)
            logging.info("Model trained successfully.")
        except Exception as e:
            logging.error(f"Error in loading data or training model: {e}")
            raise

    def setup_routes(self):
        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/forecast', methods=['POST'])
        def forecast():
            try:
                # Retrieve data from the form
                future_data = {
                    'Total_Budget': float(request.form['Total_Budget']),
                    'Revenue': float(request.form['Revenue']),
                    'Expenditure': float(request.form['Expenditure']),
                    'GDP': float(request.form['GDP']),
                    'Inflation_Rate': float(request.form['Inflation_Rate']),
                    'Unemployment_Rate': float(request.form['Unemployment_Rate']),
                    'Interest_Rate': float(request.form['Interest_Rate']),
                    'Exchange_Rate': float(request.form['Exchange_Rate']),
                }
                
                # Forecast budget using the model
                forecasted_values = self.model.forecast_data(future_data)  # Use self.model if it’s an instance method
                
                return render_template('index.html', forecasted_values=forecasted_values)
        
            except Exception as e:
                logging.error(f"Error during forecasting: {e}")
                return render_template('index.html', error="An error occurred during forecasting.")

        @app.route('/nlp', methods=['POST'])
        def nlp():
            try:
                documents = request.files.getlist('documents')
                processed_docs = DocumentProcessor.process_documents(documents)
                summaries = DocumentProcessor.summarize_documents(processed_docs)
                logging.info("NLP processing successful.")
                return render_template('index.html', summaries=summaries)
            except Exception as e:
                logging.error(f"Error in NLP processing: {e}")
                return render_template('index.html', error="NLP processing failed. Please check your documents.")

    def run(self):
        app.run(debug=True)

if __name__ == "__main__":
    app_instance = BudgetForecastingApp()
    app_instance.run()
