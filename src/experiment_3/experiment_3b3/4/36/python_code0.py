import pulp

# Data from JSON
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

# Parameters
alloy_quant = data['alloy_quant']
targets = data['target']
ratios = data['ratio']
prices = data['price']
K = len(prices)
M = len(targets)

# Linear Programming problem
problem = pulp.LpProblem("Alloy_Production_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
amounts = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(K)]

# Objective Function
problem += pulp.lpSum(prices[k] * amounts[k] for k in range(K)), "Total Cost"

# Constraints
# Total weight constraint
problem += pulp.lpSum(amounts[k] for k in range(K)) == alloy_quant, "Total_Weight_Constraint"

# Metal target constraints
for m in range(M):
    problem += pulp.lpSum(ratios[k][m] * amounts[k] for k in range(K)) == targets[m], f"Metal_{m+1}_Target_Constraint"

# Solve the problem
problem.solve()

# Output the results
amount = [pulp.value(amounts[k]) for k in range(K)]
print(f'Amounts of each alloy to purchase: {amount}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')