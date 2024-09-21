import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5], 
        [1, 3], 
        [4, 4]
    ]
}

# Number of food types (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')