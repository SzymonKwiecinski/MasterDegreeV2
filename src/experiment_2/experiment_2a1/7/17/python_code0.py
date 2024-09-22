import pulp
import json

# Given data in JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30],
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34],
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting data from the input
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Investment_Optimization", pulp.LpMaximize)

# Decision variables for the number of shares to sell
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function: maximize the expected future value of the portfolio
future_value = sum((future_price[i] * (bought[i] - sell[i])) for i in range(N))
problem += future_value

# Constraints to ensure the investor raises at least K net of costs
net_amount = sum((current_price[i] * sell[i] * (1 - transaction_rate) - 
                  (current_price[i] * sell[i] - buy_price[i] * sell[i]) * tax_rate) 
                  for i in range(N))
problem += (net_amount >= K)

# Solve the problem
problem.solve()

# Prepare output
sell_shares = [sell[i].varValue for i in range(N)]
output = {"sell": sell_shares}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')