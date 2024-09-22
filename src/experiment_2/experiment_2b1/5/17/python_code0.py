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
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Portfolio_Value", pulp.LpMaximize)

# Create decision variables for how many shares to sell
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0, upBound=bought[i], cat='Continuous') for i in range(N)]

# Objective function: maximize the expected future value of the portfolio
expected_future_value = pulp.lpSum([(futurePrice[i] * (bought[i] - sell[i])) for i in range(N)])
problem += expected_future_value

# Constraint: need to raise K net of transaction costs and taxes
net_proceeds = pulp.lpSum([((currentPrice[i] * sell[i]) * (1 - transactionRate)) - 
                            ((currentPrice[i] * sell[i] - buyPrice[i] * sell[i]) * taxRate) for i in range(N)])
problem += net_proceeds >= K

# Solve the problem
problem.solve()

# Prepare output data
result = {"sell": [pulp.value(sell[i]) for i in range(N)]}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
print(json.dumps(result))