import pulp

# Data from the JSON input
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

# Constants
alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']
K = len(price)
M = len(target)

# Define the problem
problem = pulp.LpProblem("Alloy_Production_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum([price[k] * amount[k] for k in range(K)])

# Constraint 1: Total weight of the alloy
problem += pulp.lpSum([amount[k] for k in range(K)]) == alloy_quant

# Constraint 2: Metal quantity requirements
for m in range(M):
    problem += pulp.lpSum([ratio[k][m] * amount[k] for k in range(K)]) == target[m]

# Solve the problem
problem.solve()

# Print results
print(f'Optimal Solution Found: {problem.status == pulp.LpStatusOptimal}')
for k in range(K):
    print(f'Amount of alloy {k}: {pulp.value(amount[k])} lb')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')