import pulp

# Data from JSON
data = {
    'price': [1, 2, 3], 
    'demand': [10, 20], 
    'nutrition': [
        [3, 5], 
        [1, 3], 
        [4, 4]
    ]
}

# Number of foods (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')