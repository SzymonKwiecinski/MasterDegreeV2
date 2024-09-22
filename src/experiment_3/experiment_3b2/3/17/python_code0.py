import pulp
import json

# Data in JSON format
data = json.loads('{"N": 3, "Bought": [100, 150, 80], "BuyPrice": [50, 40, 30], "CurrentPrice": [60, 35, 32], "FuturePrice": [65, 44, 34], "TransactionRate": 1.0, "TaxRate": 15.0, "K": 5000}')

# Define the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')

# Define the objective function
problem += pulp.lpSum(data['FuturePrice'][i] * (data['Bought'][i] - x[i]) for i in range(data['N'])), "Total_Profit"

# Define the constraints
problem += pulp.lpSum(
    (data['CurrentPrice'][i] * x[i] - 
     data['TransactionRate'] * data['CurrentPrice'][i] * x[i] - 
     data['TaxRate'] * pulp.lpMax(0, data['CurrentPrice'][i] * x[i] - data['BuyPrice'][i] * x[i]))
    for i in range(data['N'])) >= data['K'], "Minimum_Profit_Constraint"

# Add upper bound constraints
for i in range(data['N']):
    problem += x[i] <= data['Bought'][i], f"Upper_Bound_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')