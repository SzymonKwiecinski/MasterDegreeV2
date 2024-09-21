import pulp

# Parse the data
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

alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and number of components
num_alloys = len(prices)
num_components = len(targets)

# Initialize the problem
problem = pulp.LpProblem("Alloy_Production_Cost_Minimization", pulp.LpMinimize)

# Decision variables: x_k for each alloy k
x = [pulp.LpVariable(f"x_{k}", lowBound=0, cat='Continuous') for k in range(num_alloys)]

# Objective function: Minimize the total cost of the alloys
problem += pulp.lpSum(prices[k] * x[k] for k in range(num_alloys))

# Constraint 1: Total quantity of alloys produced is AlloyQuantity
problem += pulp.lpSum(x[k] for k in range(num_alloys)) == alloy_quantity

# Constraint 2: Each target component in the alloy must be met or exceeded
for m in range(num_components):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(num_alloys)) >= targets[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')