import pulp

# Extracting data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Parameters
K = len(data['price'])  # Number of different foods
M = len(data['demand'])  # Number of nutritional ingredients

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * quantities[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantities[k] for k in range(K)) >= data['demand'][m], f"Nutrition_{m}"

# Solve the problem
problem.solve()

# Prepare the output
result_quantities = [pulp.value(quantities[k]) for k in range(K)]

# Display results
print({"quantity": result_quantities})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')