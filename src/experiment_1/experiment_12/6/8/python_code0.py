import pulp

# Data from JSON
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Problem setup
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective Function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts']))

# Constraints
# Production time constraints for each machine
for m in range(data['NumMachines']):
    problem += (pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m])

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')