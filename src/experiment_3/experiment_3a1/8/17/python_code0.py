import pulp
import json

# Given data in JSON format
data_json = '{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}'
data = json.loads(data_json)

# Parameters
N = data['N']
bought = data['Bought']
buyPrice = data['BuyPrice']
currentPrice = data['CurrentPrice']
futurePrice = data['FuturePrice']
transactionRate = data['TransactionRate']
taxRate = data['TaxRate']
K = data['K']

# Create the linear programming problem
problem = pulp.LpProblem("Stock_Selling_Problem", pulp.LpMaximize)

# Decision variables: number of shares to sell
sell = pulp.LpVariable.dicts("sell", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((futurePrice[i] * (bought[i] - sell[i]) for i in range(N))) - \
    pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate / 100) - \
    (sell[i] * (currentPrice[i] - buyPrice[i]) * taxRate / 100) for i in range(N)))

# Constraints
problem += pulp.lpSum((currentPrice[i] * sell[i] * (1 - transactionRate / 100) - \
    (sell[i] * (currentPrice[i] - buyPrice[i]) * taxRate / 100) for i in range(N))) >= K

for i in range(N):
    problem += sell[i] <= bought[i]

# Solve the problem
problem.solve()

# Output results
sell_values = [sell[i].varValue for i in range(N)]
output = {"sell": sell_values}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(output)