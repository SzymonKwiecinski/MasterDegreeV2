import pulp

# Data from the provided JSON
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']
K = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), cat='Binary')

# Objective Function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Capacity_Constraint"

# Solve the problem
problem.solve()

# Get the results
isincluded = [x[k].varValue for k in range(K)]

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')