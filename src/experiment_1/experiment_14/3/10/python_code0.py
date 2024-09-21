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

# Constants
K = len(data['price'])
M = len(data['demand'])

# Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)]), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * x[k] for k in range(K)]) >= data['demand'][m], f"Nutrition_Requirement_{m}"

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')