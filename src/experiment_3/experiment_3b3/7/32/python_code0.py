import pulp

# Data input
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
q = [pulp.LpVariable(f'q_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective function
problem += pulp.lpSum(data['Profit'][k] * q[k] for k in range(data['NumProducts']))

# Constraints
for s in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][s] * q[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][s]

# Solve the problem
problem.solve()

# Output the results
quantity = [pulp.value(q[k]) for k in range(data['NumProducts'])]
print("Quantities to produce:", quantity)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')