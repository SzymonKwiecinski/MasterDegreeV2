import pulp

# Data from provided JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Create a problem variable
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision Variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m], f"Nutrient_Requirement_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')