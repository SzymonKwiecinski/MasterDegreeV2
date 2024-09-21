import pulp

# Data
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

# Problem Definition
problem = pulp.LpProblem("Alloy_Production_Minimization", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(len(data['price']))]

# Objective Function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(len(data['price'])))

# Constraint 1: Total quantity of alloys produced
problem += pulp.lpSum(x) == data['alloy_quant'], "Total_Alloys_Quantity"

# Constraint 2: Meet or exceed quantity of target components
for m in range(len(data['target'])):
    problem += pulp.lpSum(data['ratio'][k][m] * x[k] for k in range(len(data['price']))) >= data['target'][m], f"Target_Component_{m+1}"

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')