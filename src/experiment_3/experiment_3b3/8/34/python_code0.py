import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Sets
K = range(len(data['price']))  # Set of foods
M = range(len(data['demand']))  # Set of nutritional ingredients

# Problem
problem = pulp.LpProblem("Food_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in K]

# Objective Function
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in K), "Total Cost"

# Constraints
for m in M:
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in K) >= data['demand'][m], f'Nutrient_{m}_Demand'

# Solve
problem.solve()

# Print the Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')