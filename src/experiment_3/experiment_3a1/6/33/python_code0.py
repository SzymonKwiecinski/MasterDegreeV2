import pulp

# Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
value = data['value']
size = data['size']
K = len(value)

# Create the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective function
problem += pulp.lpSum(value[k] * x[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(size[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Output the results
included = [int(x[k].varValue) for k in range(K)]
print(f'Included items: {included}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')