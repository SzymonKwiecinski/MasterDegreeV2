import pulp

# Data from the input
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Number of food items
K = len(data['price'])

# Number of nutritional constraints
M = len(data['demand'])

# Create the Linear Programming problem
problem = pulp.LpProblem("Minimize_Food_Costs", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total Cost"

# Nutritional Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutritional_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')