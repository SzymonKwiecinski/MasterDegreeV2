import pulp
import json

# Input data
data = {
    'N': 3, 
    'Bought': [100, 150, 80], 
    'BuyPrice': [50, 40, 30], 
    'CurrentPrice': [60, 35, 32], 
    'FuturePrice': [65, 44, 34], 
    'TransactionRate': 1.0, 
    'TaxRate': 15.0, 
    'K': 5000
}

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
problem = pulp.LpProblem("Sell_Shares_Problem", pulp.LpMaximize)

# Variables: number of shares to sell for each stock
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, upBound=None)

# Objective function: maximize the expected portfolio value next year minus the total selling costs
expected_future_value = pulp.lpSum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
total_selling_price = pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate)) for i in range(N))
capital_gains_tax = pulp.lpSum((currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate for i in range(N))

# The objective is to maximize the expected future value
problem += expected_future_value - total_selling_price + capital_gains_tax

# Constraint: the final amount after selling shares must be equal or greater than K
problem += total_selling_price - capital_gains_tax >= K

# Solve the problem
problem.solve()

# Collecting results
sell_shares = [sell[i].varValue for i in range(N)]

# Output results
output = {
    "sell": sell_shares
}

# Print results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')