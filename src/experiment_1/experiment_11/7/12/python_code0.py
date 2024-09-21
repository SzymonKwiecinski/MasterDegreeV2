import pulp

# Input data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quantity = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']

K = len(prices)  # number of alloys
M = len(targets) # number of target components

# Create the optimization problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total_Cost"

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == alloy_quantity, "Total_Quantity"

# Constraints 2: Meet or exceed target component quantities
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * x[k] for k in range(K)) >= targets[m], f"Target_Component_{m+1}"

# Solve the problem
problem.solve()

# Display the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')