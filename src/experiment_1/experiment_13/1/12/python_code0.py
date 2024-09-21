import pulp

# Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [[0.1, 0.9], [0.25, 0.75], [0.5, 0.5], [0.75, 0.25], [0.95, 0.05]],
    'price': [5, 4, 3, 2, 1.5]
}

# Constants
K = len(data['price'])  # Number of alloys
M = len(data['target'])  # Number of target components
AlloyQuantity = data['alloy_quant']
Target = data['target']
Ratio = data['ratio']
Price = data['price']

# Create the LP problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "TotalCost"

# Constraints
# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x[k] for k in range(K)) == AlloyQuantity, "TotalAlloyQuantity"

# Constraint 2: Meet or exceed target components
for m in range(M):
    problem += pulp.lpSum(Ratio[k][m] * x[k] for k in range(K)) >= Target[m], f"TargetComponent_{m}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')