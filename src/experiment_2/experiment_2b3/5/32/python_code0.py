import pulp

# Input Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Problem Definition
problem = pulp.LpProblem("Profit Maximization", pulp.LpMaximize)

# Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective Function: Maximize total profit
problem += pulp.lpSum([data['Profit'][k] * quantities[k] for k in range(data['NumProducts'])])

# Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum([data['ProduceTime'][k][s] * quantities[k] for k in range(data['NumProducts'])]) <= data['AvailableTime'][s]

# Solve the problem
problem.solve()

# Extract the results
results = {
    "quantity": [quantities[k].varValue for k in range(data['NumProducts'])]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')