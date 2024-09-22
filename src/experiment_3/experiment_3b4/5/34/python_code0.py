import pulp

# Data from JSON format
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Initialize the problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(data['price'][k] * quantities[k] for k in range(K)), "Total Cost"

# Nutritional constraints
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * quantities[k] for k in range(K)) 
                >= data['demand'][m], f'Nutrient_{m}_Requirement')

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')