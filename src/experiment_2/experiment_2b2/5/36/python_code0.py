import pulp

# Read the data
data = {'alloy_quant': 1000, 'target': [300, 700], 'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]], 'price': [5, 4, 3, 2, 1.5]}
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

# Number of metals and alloys
M = len(target)
K = len(price)

# Initialize the problem
problem = pulp.LpProblem("Alloy_Manufacturing", pulp.LpMinimize)

# Decision variables: The amount of each alloy k to use
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the total cost of alloys
total_cost = pulp.lpSum([price[k] * amount[k] for k in range(K)])
problem += total_cost

# Constraints: Ensure the required percentage of each metal
for m in range(M):
    metal_constraint = pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m]
    problem += metal_constraint

# Solve the problem
problem.solve()

# Prepare the output data
output = {"amount": [pulp.value(amount[k]) for k in range(K)]}
print(output)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')