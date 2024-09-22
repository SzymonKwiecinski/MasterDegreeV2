import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting variables from data
N = data['N']
bought = data['Bought']
buy_price = data['BuyPrice']
current_price = data['CurrentPrice']
future_price = data['FuturePrice']
transaction_rate = data['TransactionRate'] / 100
tax_rate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Portfolio_Selling_Problem", pulp.LpMaximize)

# Decision variables: the number of shares to sell
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=pulp.LpInfinity)

# Objective function: Maximize future portfolio value
portfolio_value = sum((future_price[i] * (bought[i] - sell[i])) for i in range(N))
problem += portfolio_value

# Constraints to ensure net amount raised is at least K
net_amount = sum((current_price[i] * sell[i] * (1 - transaction_rate) - 
                  (current_price[i] * sell[i] - buy_price[i] * sell[i]) * tax_rate) for i in range(N))
problem += net_amount >= K

# Solve the problem
problem.solve()

# Collect results
sell_output = [sell[i].varValue for i in range(N)]

# Output the results
output = {
    "sell": sell_output,
}

print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')