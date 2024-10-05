import pulp

# Data from the provided JSON format.
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

alloy_quant = data['alloy_quant']
target = data['target']
ratio = data['ratio']
price = data['price']

K = len(price)  # Number of available alloys
M = len(target)  # Number of metals in the target alloy composition

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Alloy_Cost", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(K), lowBound=0)

# Objective function
problem += pulp.lpSum(price[k] * amount[k] for k in range(K)), "Total_Cost"

# Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == alloy_quant, "Total_Weight"

# Metal composition constraints
for m in range(M):
    problem += pulp.lpSum(ratio[k][m] * amount[k] for k in range(K)) >= target[m], f"Composition_Constraint_{m}"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')