import pulp

# Data
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Create the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective Function
profit = pulp.lpSum([data['Profit'][k] * x[k] for k in range(data['NumProducts'])])
problem += profit

# Constraints
# Production time constraints for each machine
for m in range(data['NumMachines']):
    problem += pulp.lpSum([data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])]) <= data['AvailableTime'][m]

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')