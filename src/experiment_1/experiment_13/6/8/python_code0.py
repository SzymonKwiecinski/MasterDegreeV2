import pulp

# Data from the provided JSON format
data = {
    'NumProducts': 2,
    'NumMachines': 2,
    'ProduceTime': [[1, 3], [2, 1]],
    'AvailableTime': [200, 100],
    'Profit': [20, 10]
}

# Create a linear programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['NumProducts']), 0)

# Objective function
problem += pulp.lpSum(data['Profit'][k] * x[k] for k in range(data['NumProducts'])), "Total_Profit"

# Constraints for available time on each machine
for m in range(data['NumMachines']):
    problem += (pulp.lpSum(data['ProduceTime'][k][m] * x[k] for k in range(data['NumProducts'])) <= data['AvailableTime'][m]), f"Machine_{m+1}_Time_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')