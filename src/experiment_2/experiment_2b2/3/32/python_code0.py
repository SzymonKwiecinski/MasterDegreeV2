import pulp

# Load data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective function
problem += pulp.lpSum(quantity[k] * data['Profit'][k] for k in range(data['NumProducts']))

# Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(quantity[k] * data['ProduceTime'][k][s] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

# Solve
problem.solve()

# Output
output = {'quantity': [pulp.value(quantity[k]) for k in range(data['NumProducts'])]}
print(output)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')