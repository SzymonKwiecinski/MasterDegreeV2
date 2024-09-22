import pulp
import json

# Given data in JSON format
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting values from data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Expected_Portfolio_Value", pulp.LpMaximize)

# Create decision variables for selling shares
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0)

# Objective function: maximize the expected value of the portfolio next year
expected_portfolio_value = pulp.lpSum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_portfolio_value

# Constraints to ensure the net amount raised meets or exceeds K
net_amount = pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate) - 
                        (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate) 
                        for i in range(N))
problem += net_amount >= K

# Constraints on how many shares can be sold (cannot sell more than owned)
for i in range(N):
    problem += sell[i] <= bought[i]

# Solve the problem
problem.solve()

# Prepare results
sell_result = [sell[i].varValue for i in range(N)]

# Output result
result = {
    "sell": sell_result
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')