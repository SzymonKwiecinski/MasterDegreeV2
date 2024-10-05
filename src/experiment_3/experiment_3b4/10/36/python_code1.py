import pulp

# Load data
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

# Extract data
alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(ratios)
M = len(targets)

# Create problem variable
problem = pulp.LpProblem("Alloy_Production_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0) for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints
# Total Alloy Production Requirement
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quant

# Metal Composition Requirement
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) == targets[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')