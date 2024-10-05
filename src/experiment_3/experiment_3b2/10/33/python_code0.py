import pulp

# Data provided
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * isincluded[k] for k in range(K)), "Total_Value"

# Capacity constraint
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')