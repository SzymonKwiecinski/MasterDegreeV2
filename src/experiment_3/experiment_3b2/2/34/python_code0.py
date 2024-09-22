import pulp

# Data from the provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of different foods (K) and nutritional requirements (M)
K = len(data['price'])
M = len(data['demand'])

# Create the linear programming problem
problem = pulp.LpProblem("Diet_Optimization", pulp.LpMinimize)

# Decision variables: quantity of each food
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints: Nutritional requirements
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutritional_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')