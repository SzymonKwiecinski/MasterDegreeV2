import pulp
import json

# Data in JSON format
data_json = '{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}'
data = json.loads(data_json)

# Define the problem
problem = pulp.LpProblem("Investor_Stock_Sale", pulp.LpMaximize)

# Variables
sold = pulp.LpVariable.dicts("sell", range(data['N']), lowBound=0)

# Objective Function
problem += pulp.lpSum([data['FuturePrice'][i] * (data['Bought'][i] - sold[i]) for i in range(data['N'])])

# Constraints
problem += (pulp.lpSum([(data['CurrentPrice'][i] * sold[i] * (1 - data['TransactionRate'] / 100)) - 
                         (sold[i] * data['BuyPrice'][i] * (1 - data['TaxRate'] / 100)) for i in range(data['N'])]) >= data['K'])

for i in range(data['N']):
    problem += (sold[i] <= data['Bought'][i])

# Solve the problem
problem.solve()

# Output the results
sell = [pulp.value(sold[i]) for i in range(data['N'])]
print(f'Sell: {sell}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')