import pulp

# Data input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Indices
K = len(data['price'])  # Number of foods
M = len(data['demand'])  # Number of nutritional ingredients

# Create the problem
problem = pulp.LpProblem("Diet_Problem", pulp.LpMinimize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Nutritional Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m],
        f"Nutritional_Requirement_{m}"
    )

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')