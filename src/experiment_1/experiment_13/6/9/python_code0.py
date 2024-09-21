import pulp

# Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Create a problem instance
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, upBound=1, cat='Binary')

# Objective function
problem += pulp.lpSum([values[k] * x[k] for k in range(K)]), "Total_Value"

# Constraint: total size must not exceed capacity
problem += pulp.lpSum([sizes[k] * x[k] for k in range(K)]) <= C, "Total_Size_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')