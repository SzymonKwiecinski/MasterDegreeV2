import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of food types (K) and nutrients (M)
K = len(data['price'])
M = len(data['demand'])

# Create a linear programming problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables: number of units purchased from each food type
x = pulp.LpVariable.dicts("x", range(K), lowBound=0, cat='Continuous')

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints: Total nutrients must meet or exceed demand
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f"Nutrient_{m+1}_Demand"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')