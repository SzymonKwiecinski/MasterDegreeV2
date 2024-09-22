import pulp
import json

# Given data
data = {'N': 3, 'Bought': [100, 150, 80], 'BuyPrice': [50, 40, 30], 
        'CurrentPrice': [60, 35, 32], 'FuturePrice': [65, 44, 34], 
        'TransactionRate': 1.0, 'TaxRate': 15.0, 'K': 5000}

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100  # Convert percentage to decimal
taxRate = data['TaxRate'] / 100  # Convert percentage to decimal
K = data['K']

# Create the LP problem
problem = pulp.LpProblem("Investment_Optimization", pulp.LpMaximize)

# Decision variables: sell_i for each stock i
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i]) for i in range(N)]

# Objective function: maximize future portfolio value
expected_future_value = sum((futurePrice[i] * (bought[i] - sell[i])) for i in range(N))
problem += expected_future_value

# Constraint: raise an amount of money K net of capital gains and transaction costs
net_proceeds = sum((currentPrice[i] * sell[i] * (1 - transactionRate) - 
                    (currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate) for i in range(N))
problem += (net_proceeds >= K)

# Solve the problem
problem.solve()

# Prepare the output
sell_amounts = [sell[i].varValue for i in range(N)]
output = {"sell": sell_amounts}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')