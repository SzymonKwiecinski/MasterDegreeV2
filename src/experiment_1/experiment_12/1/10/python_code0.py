import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of different types of food
M = len(data['demand'])  # Number of nutrients to consider

# Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total Cost"

# Constraints
# Nutrient demand constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_{m}_Demand"

# Solve problem
problem.solve()

# Results
print(f'Status: {pulp.LpStatus[problem.status]}')
for k in range(K):
    print(f'Amount of Food Type {k+1}: {x[k].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')