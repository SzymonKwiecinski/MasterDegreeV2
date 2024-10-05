import pulp

# Data from the JSON
data = {
    'alloy_quant': 1000, 
    'target': [300, 700], 
    'ratio': [
        [0.1, 0.9], 
        [0.25, 0.75], 
        [0.5, 0.5], 
        [0.75, 0.25], 
        [0.95, 0.05]
    ], 
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and metals
num_alloys = len(prices)
num_metals = len(target)

# Define the LP problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(num_alloys)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(num_alloys))

# Constraint: Total weight of alloys
problem += pulp.lpSum(x[k] for k in range(num_alloys)) == alloy_quant

# Constraints: Target compositions for each metal
for m in range(num_metals):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(num_alloys)) == target[m]

# Solve the problem
problem.solve()

# Print the results
amounts = [pulp.value(x[k]) for k in range(num_alloys)]
print(f'Alloy amounts: {amounts}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')