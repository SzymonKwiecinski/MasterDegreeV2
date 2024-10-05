import pulp
import json

# Load the data
data = '''{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}'''
data = json.loads(data)

N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate'] / 100
taxRate = data['TaxRate'] / 100
K = data['K']

# Define the Linear Programming problem
problem = pulp.LpProblem("Investor_Problem", pulp.LpMaximize)

# Decision variables
sell = [pulp.LpVariable(f'sell_{i}', lowBound=0) for i in range(N)]

# Objective function
expected_value = pulp.lpSum([(bought[i] - sell[i]) * futurePrice[i] for i in range(N)])
problem += expected_value

# Constraints

# Raise at least K money
raised_money = pulp.lpSum(
    [(sell[i] * currentPrice[i] * (1 - transactionRate)) - 
    (sell[i] * (currentPrice[i] - buyPrice[i]) * taxRate) for i in range(N)]
)
problem += raised_money >= K

# Solve the problem
problem.solve()

# Gather results
results = {
    "sell": [pulp.value(sell[i]) for i in range(N)]
}

# Output the results and objective value
print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')