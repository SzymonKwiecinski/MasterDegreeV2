import pulp

# Data from JSON format
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Create the problem variable
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K)), "Total_Cost"

# Constraints for nutritional demands
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m]), f"Nutritional_Demand_{m+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')