import pulp

# Data provided in the problem
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Extracting values from the data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(price)
M = len(demand)

# Create a problem variable for the Linear Programming problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum([price[k] * x[k] for k in range(K)]), "Total Cost"

# Constraints: Nutrient demands must be satisfied
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * x[k] for k in range(K)]) >= demand[m], f"Demand_{m}"

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')