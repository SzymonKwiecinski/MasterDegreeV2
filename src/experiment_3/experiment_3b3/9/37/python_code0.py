import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Indices
K = len(data['profit'])
S = len(data['capacity'])

# Initialize the problem
problem = pulp.LpProblem("Spare_Automobile_Parts_Production", pulp.LpMaximize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
profit = data['profit']
objective = pulp.lpSum(profit[k] * quantity[k] for k in range(K))
problem += objective

# Constraints
time = data['time']
capacity = data['capacity']
for s in range(S):
    constraint = pulp.lpSum(time[k][s] * quantity[k] for k in range(K))
    problem += constraint <= capacity[s]

# Solve the problem
problem.solve()

# Output the quantities
quantities = [pulp.value(quantity[k]) for k in range(K)]
print("Quantities of each spare part to be produced:", quantities)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')