import pulp

# Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the linear programming problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Capacity constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')