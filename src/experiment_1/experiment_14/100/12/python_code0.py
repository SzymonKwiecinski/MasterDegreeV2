import pulp

# Data from the JSON input
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Extract data
AlloyQuantity = data['alloy_quant']
Targets = data['target']
Ratios = data['ratio']
Prices = data['price']

# Number of alloys and components
K = len(Prices)
M = len(Targets)

# Define the LP problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables: quantities of each alloy
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([Prices[k] * x[k] for k in range(K)])

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum([x[k] for k in range(K)]) == AlloyQuantity

# Constraint 2: Meet or exceed the target components in the alloy
for m in range(M):
    problem += pulp.lpSum([Ratios[k][m] * x[k] for k in range(K)]) >= Targets[m]

# Solve the problem
problem.solve()

# Print the results
print("Status:", pulp.LpStatus[problem.status])

for k in range(K):
    print(f'x_{k} = {pulp.value(x[k])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')