import pulp

# Data
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Problem Definition
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
K = range(len(values))
isincluded = pulp.LpVariable.dicts("isincluded", K, cat='Binary')

# Objective Function
problem += pulp.lpSum(values[k] * isincluded[k] for k in K), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * isincluded[k] for k in K) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')