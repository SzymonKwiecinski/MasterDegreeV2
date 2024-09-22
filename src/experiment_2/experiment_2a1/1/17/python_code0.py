import pulp
import json

# Data input
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting variables from the data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create a linear programming problem
problem = pulp.LpProblem("Portfolio_Selling_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function: Maximize expected future value
expected_future_value = sum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_future_value

# Constraints
# The amount raised must cover the net K needed after transaction costs and taxes on capital gains
net_raised = sum((currentPrice[i] * sell[i] * (1 - transactionRate) * (1 - taxRate * (currentPrice[i] - buyPrice[i]) / currentPrice[i])) for i in range(N))
problem += net_raised >= K

# Solve the problem
problem.solve()

# Output the results
sell_amounts = [pulp.value(sell[i]) for i in range(N)]
output = {
    "sell": sell_amounts
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')