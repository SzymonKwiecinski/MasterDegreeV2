import pulp

# Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}

# Parameters
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Create the problem variable
problem = pulp.LpProblem("KnapsackProblem", pulp.LpMaximize)

# Decision Variables
isincluded = pulp.LpVariable.dicts("isincluded", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum([values[k] * isincluded[k] for k in range(K)]), "TotalValue"

# Constraints
problem += pulp.lpSum([sizes[k] * isincluded[k] for k in range(K)]) <= C, "CapacityConstraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')