import pulp

# Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraint
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the results
for k in range(K):
    print(f'Item {k + 1} included: {x[k].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')