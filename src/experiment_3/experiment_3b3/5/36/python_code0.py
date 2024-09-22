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

# Initialize the problem
problem = pulp.LpProblem("AlloyProduction", pulp.LpMinimize)

# Variables
num_alloys = len(data['price'])
x = pulp.LpVariable.dicts("Alloy", range(num_alloys), lowBound=0)

# Objective Function
problem += pulp.lpSum([data['price'][k] * x[k] for k in range(num_alloys)])

# Constraints
# Total weight constraint
problem += pulp.lpSum([x[k] for k in range(num_alloys)]) == data['alloy_quant']

# Metal composition constraints
num_metals = len(data['target'])
for m in range(num_metals):
    problem += pulp.lpSum([data['ratio'][k][m] * x[k] for k in range(num_alloys)]) == data['target'][m]

# Solve the problem
problem.solve()

# Output the results
solution = [x[k].varValue for k in range(num_alloys)]
print(f'Amounts of each alloy to purchase: {solution}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')