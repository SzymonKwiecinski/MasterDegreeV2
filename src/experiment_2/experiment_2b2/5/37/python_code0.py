import pulp

# Problem Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

K = len(profit)  # number of parts
S = len(capacity)  # number of shops

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
profit_expr = pulp.lpSum([profit[k] * quantity[k] for k in range(K)])
problem += profit_expr, "Total_Profit"

# Constraints
for s in range(S):
    problem += (
        pulp.lpSum([time[k][s] * quantity[k] for k in range(K)]) <= capacity[s],
        f"Capacity_Shop_{s}"
    )

# Solve
problem.solve()

# Outputs
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')