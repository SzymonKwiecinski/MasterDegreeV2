import pulp

# Data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Unpack the data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Problem
problem = pulp.LpProblem("Food_Minimization", pulp.LpMinimize)

# Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantities[k] for k in range(K)) >= demands[m], f"Nutrient_{m}_Constraint"

# Solve the problem
problem.solve()

# Results
result = {
    "quantity": [quantities[k].varValue for k in range(K)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')