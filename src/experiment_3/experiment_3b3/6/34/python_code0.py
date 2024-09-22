import pulp

# Data from <DATA>
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],  # Food 1 provides per unit
        [1, 3],  # Food 2 provides per unit
        [4, 4]   # Food 3 provides per unit
    ]
}

# Initialize the Linear Program
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Number of foods (K)
K = len(data['price'])

# Number of nutrients (M)
M = len(data['demand'])

# Decision variables: x_k >= 0 for all k
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(K)])

# Constraints: Ensure nutritional requirements are met
for m in range(M):
    problem += pulp.lpSum([data['nutrition'][k][m] * x[k] for k in range(K)]) >= data['demand'][m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the quantities to purchase
quantities = [pulp.value(x_k) for x_k in x]
print("Quantities to purchase:", quantities)