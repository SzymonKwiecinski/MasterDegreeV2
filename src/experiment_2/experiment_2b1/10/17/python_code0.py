import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

# Extracting data
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the problem
problem = pulp.LpProblem("Portfolio_Optimization", pulp.LpMaximize)

# Define decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function: maximize the future value of the portfolio
expected_future_value = pulp.lpSum([(futurePrice[i] * (bought[i] - sell[i])) for i in range(N)])
problem += expected_future_value

# Constraints: the amount raised after selling must meet or exceed K
amount_raised = pulp.lpSum([
    (currentPrice[i] * sell[i]) * (1 - transactionRate) - 
    (taxRate * (currentPrice[i] * sell[i] - buyPrice[i] * sell[i])) for i in range(N)
])
problem += amount_raised >= K

# Solve the problem
problem.solve()

# Prepare output
sell_result = [sell[i].varValue for i in range(N)]
output = {"sell": sell_result}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')