import pulp

# Input Data
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
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices) # number of different available alloys
M = len(targets) # number of metals in the alloy

# Create the LP problem
problem = pulp.LpProblem("Alloy_Mixing_Problem", pulp.LpMinimize)

# Define variables for the amount of each alloy
amount_vars = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective function: Minimize the cost
problem += pulp.lpSum([prices[k] * amount_vars[k] for k in range(K)])

# Constraints
# Constraint for total quantity of alloy
problem += pulp.lpSum(amount_vars) == alloy_quant

# Constraints for each metal content
for m in range(M):
    problem += pulp.lpSum([ratios[k][m] * amount_vars[k] for k in range(K)]) == targets[m]

# Solve the problem
problem.solve()

# Collect the results
output = {
    "amount": [pulp.value(amount_vars[k]) for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')