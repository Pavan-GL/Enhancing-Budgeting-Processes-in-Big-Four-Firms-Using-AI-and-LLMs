import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate a range of years
years = np.arange(2000, 2023)  # From 2000 to 2022

# Create a list to hold economic indicator data
economic_data = []

# Simulate economic data for each year
for year in years:
    gdp = np.random.randint(3000000, 30000000)  # GDP in crores
    inflation_rate = np.random.uniform(3.0, 8.0)  # Inflation rate between 3% and 8%
    unemployment_rate = np.random.uniform(3.0, 10.0)  # Unemployment rate between 3% and 10%
    interest_rate = np.random.uniform(4.0, 8.0)  # Interest rate between 4% and 8%
    exchange_rate = np.random.uniform(60, 80)  # Exchange rate (INR to USD)

    economic_data.append({
        'Year': year,
        'GDP': gdp,
        'Inflation_Rate': round(inflation_rate, 2),
        'Unemployment_Rate': round(unemployment_rate, 2),
        'Interest_Rate': round(interest_rate, 2),
        'Exchange_Rate': round(exchange_rate, 2)
    })

# Create a DataFrame
economic_df = pd.DataFrame(economic_data)

# Repeat to generate more rows (to reach ~5000 rows)
economic_df = pd.concat([economic_df] * (5000 // len(economic_df)), ignore_index=True)

# Shuffle the DataFrame
economic_df = economic_df.sample(frac=1).reset_index(drop=True)

# Save to CSV
economic_df.to_csv('D:\Enhancing Budgeting Processes in Big Four Firms Using AI and LLMs\data\economic_indicators.csv', index=False)

print("Generated economic indicators data with", len(economic_df), "rows.")
