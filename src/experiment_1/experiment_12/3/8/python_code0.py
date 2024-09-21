import pulp

# Data provided
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Create the LP problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective function
objective = pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts']))
problem += objective

# Constraints
# Production time constraints for each machine
for m in range(data['NumMachines']):
    constraint = pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m]
    problem += constraint

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')