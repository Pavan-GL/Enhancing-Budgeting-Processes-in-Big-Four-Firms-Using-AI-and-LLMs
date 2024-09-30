import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate a range of years
years = np.arange(2000, 2023)  # From 2000 to 2022

# Create a list to hold budget data
budget_data = []

# Simulate budget data for each year
for year in years:
    total_budget = np.random.randint(500000, 3000000)  # Total budget in crores
    revenue = np.random.randint(int(total_budget * 0.5), int(total_budget * 0.8))  # Revenue as 50-80% of total budget
    expenditure = total_budget - revenue  # Expenditure is the remainder
    deficit = np.random.randint(0, int(total_budget * 0.1))  # Deficit can be up to 10% of total budget
    gdp = np.random.randint(3000000, 20000000)  # GDP in crores

    budget_data.append({
        'Year': year,
        'Total_Budget': total_budget,
        'Revenue': revenue,
        'Expenditure': expenditure,
        'Deficit': deficit,
        'GDP': gdp
    })

# Create a DataFrame
budget_df = pd.DataFrame(budget_data)

# Repeat to generate more rows (to reach ~5000 rows)
budget_df = pd.concat([budget_df] * (5000 // len(budget_df)), ignore_index=True)

# Shuffle the DataFrame
budget_df = budget_df.sample(frac=1).reset_index(drop=True)

# Save to CSV
budget_df.to_csv('D:\Enhancing Budgeting Processes in Big Four Firms Using AI and LLMs\data\historical_budget_data.csv', index=False)

print("Generated historical budget data with", len(budget_df), "rows.")
