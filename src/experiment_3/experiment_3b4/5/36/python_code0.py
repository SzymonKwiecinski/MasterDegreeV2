import pulp

# Problem data
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

# Initialize the LP problem
problem = pulp.LpProblem("Alloy_Mixture_Problem", pulp.LpMinimize)

# Number of alloys and metals
K = len(data['price'])  # number of different alloys
M = len(data['target'])  # number of metals

# Decision Variables
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost of purchasing the alloys
problem += pulp.lpSum(data['price'][k] * amount[k] for k in range(K))

# Constraints
# Total weight constraint
problem += pulp.lpSum(amount[k] for k in range(K)) == data['alloy_quant']

# Composition constraints for each metal
for m in range(M):
    problem += pulp.lpSum(data['ratio'][k][m] * amount[k] for k in range(K)) == data['target'][m]

# Solve the problem
problem.solve()

# Print the objective value (total cost)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')