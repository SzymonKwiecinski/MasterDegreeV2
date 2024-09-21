import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],  # Nutrition in food 1
        [1, 3],  # Nutrition in food 2
        [4, 4]   # Nutrition in food 3
    ]
}

# Number of foods (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Parameters
Price = data['price']
Demand = data['demand']
Nutrition = data['nutrition']

# Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([Price[k] * x[k] for k in range(K)])

# Constraints
# Nutrient demand constraints
for m in range(M):
    problem += (
        pulp.lpSum([Nutrition[k][m] * x[k] for k in range(K)]) >= Demand[m],
        f"Nutrient_Requirement_{m}"
    )

# Solve
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')