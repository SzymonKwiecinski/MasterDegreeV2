import pulp

# Input data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Create the problem variable
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Create binary decision variables
x = pulp.LpVariable.dicts("x", range(K), 0, 1, pulp.LpBinary)

# Objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraint: Total size must not exceed capacity
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Total_Size_Constraint"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')