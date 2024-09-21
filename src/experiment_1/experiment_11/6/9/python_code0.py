import pulp

# Data from the provided JSON format
data = {'C': 10, 'value': [10, 20], 'size': [8, 6]}
C = data['C']
values = data['value']
sizes = data['size']

# Number of items
K = len(values)

# Define the problem
problem = pulp.LpProblem("Knapsack_Problem", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("item", range(K), cat='Binary')

# Define the objective function
problem += pulp.lpSum(values[k] * x[k] for k in range(K)), "Total_Value"

# Define the constraints
problem += pulp.lpSum(sizes[k] * x[k] for k in range(K)) <= C, "Total_Size_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')