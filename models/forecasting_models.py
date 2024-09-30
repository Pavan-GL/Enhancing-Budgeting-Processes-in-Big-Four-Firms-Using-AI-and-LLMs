import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
import logging
import os

# Configure logging
logging.basicConfig(
    filename='logs/model_training.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ForecastingModel:
    def __init__(self):
        self.model = None
    
    def train(self, budget_data, economic_data):
        try:
            # Preprocessing and merging data
            logging.info("Merging budget and economic data...")
            merged_data = pd.merge(budget_data, economic_data, on='Year')

            # Log the columns of the merged data
            logging.info(f"Merged Data Columns: {merged_data.columns.tolist()}")

            # Check original data columns
            logging.info(f"Budget Data Columns: {budget_data.columns.tolist()}")
            logging.info(f"Economic Data Columns: {economic_data.columns.tolist()}")

            # Define features and target variable
            target_variable_name = 'Total_Budget'  # Set this to the actual target variable name

            # Check if the target variable is in the merged data
            if target_variable_name not in merged_data.columns:
                raise ValueError(f"Target variable '{target_variable_name}' not found in merged data.")

            X = merged_data.drop(target_variable_name, axis=1)
            y = merged_data[target_variable_name]
            
            # Split the data
            logging.info("Splitting data into training and testing sets...")
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Build the model
            logging.info("Building the model...")
            self.model = tf.keras.Sequential([
                tf.keras.layers.Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
                tf.keras.layers.Dense(32, activation='relu'),
                tf.keras.layers.Dense(1)  # Output layer for regression
            ])
            self.model.compile(optimizer='adam', loss='mean_squared_error')

            # Train the model
            logging.info("Training the model...")
            self.model.fit(X_train, y_train, epochs=100, batch_size=32)

            # Save the model
            model_file_path = 'models/forecasting_model.h5'
            logging.info(f"Saving the model to {model_file_path}...")
            self.model.save(model_file_path)

            logging.info("Model training and saving completed successfully.")
        except Exception as e:
            logging.error(f"Error during model training: {e}")
            raise




    def forecast_data(self, future_data):
        try:
            # Prepare future data for prediction
            future_df = pd.DataFrame([future_data])  # Convert input to DataFrame
            logging.info("Making predictions on future data...")
            predictions = self.model.predict(future_df)
            return predictions[0]  # Return the first prediction
        except Exception as e:
            logging.error(f"Error during forecasting: {e}")
            raise

# Example usage (This would be in your main application code)
if __name__ == "__main__":
    # Create logs and models directory if they don't exist
    os.makedirs('logs', exist_ok=True)
    os.makedirs('models', exist_ok=True)

    # Assume budget_data and economic_data are already loaded
    budget_data = pd.read_csv('D:\Enhancing Budgeting Processes in Big Four Firms Using AI and LLMs\data\historical_budget_data.csv')
    economic_data = pd.read_csv('D:\Enhancing Budgeting Processes in Big Four Firms Using AI and LLMs\data\economic_indicators.csv')

    forecasting_model = ForecastingModel()
    forecasting_model.train(budget_data, economic_data)

    # Example future data for forecasting
    future_data_example = {
    'Total_Budget': 2500000,          # Example future budget in crores
    'Revenue': 1800000,               # Example revenue in crores
    'Expenditure': 700000,             # Example expenditure in crores
    'GDP': 20000000,                  # Example GDP in crores
    'Inflation_Rate': 5.5,            # Example inflation rate in percentage
    'Unemployment_Rate': 6.0,         # Example unemployment rate in percentage
    'Interest_Rate': 6.5,             # Example interest rate in percentage
    'Exchange_Rate': 75               # Example exchange rate (INR to USD)
}

    # Perform forecasting
    prediction = forecasting_model.forecast(future_data_example)
    print("Forecasted Budget:", prediction)
