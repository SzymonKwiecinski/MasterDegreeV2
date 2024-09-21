import pulp

# Load data
data = {'NumProducts': 2, 'NumMachines': 2, 'ProduceTime': [[1, 3], [2, 1]], 'AvailableTime': [200, 100], 'Profit': [20, 10]}

# Create a linear programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(data['NumProducts'])]

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

# Constraints
# Production time constraints for each machine
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m], f'Machine_{m}_Time'

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')