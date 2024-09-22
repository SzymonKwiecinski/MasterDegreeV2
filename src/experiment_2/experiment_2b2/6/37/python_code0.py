import pulp

# Data Input
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

times = data['time']
profits = data['profit']
capacities = data['capacity']

K = len(profits)
S = len(capacities)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
profit_expr = pulp.lpSum([profits[k] * quantities[k] for k in range(K)])
problem += profit_expr

# Constraints
for s in range(S):
    time_expr = pulp.lpSum([times[k][s] * quantities[k] for k in range(K)])
    problem += time_expr <= capacities[s], f'Capacity_Constraint_Shop_{s}'

# Solve
problem.solve()

# Output
output = {
    "quantity": [pulp.value(quantities[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')