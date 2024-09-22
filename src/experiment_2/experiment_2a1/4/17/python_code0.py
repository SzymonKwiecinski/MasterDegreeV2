import pulp
import json

# Input data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100.0  # converting percentage to decimal
taxRate = data['TaxRate'] / 100.0  # converting percentage to decimal
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("SellStocks", pulp.LpMaximize)

# Define the decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Define the objective function
# Maximize the future value of the remaining stocks
objective = pulp.lpSum(((bought[i] - sell[i]) * futurePrice[i]) for i in range(N))
problem += objective

# Define the constraints
# The net amount raised must cover K after transaction costs and taxes
net_amount = pulp.lpSum((sell[i] * currentPrice[i] * (1 - transactionRate) -
                          (sell[i] * currentPrice[i] - sell[i] * buyPrice[i]) * taxRate)
                         for i in range(N))
problem += net_amount >= K

# Solve the problem
problem.solve()

# Output the result
sell_results = [pulp.value(sell[i]) for i in range(N)]
output = {"sell": sell_results}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')