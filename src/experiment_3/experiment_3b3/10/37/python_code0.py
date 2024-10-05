import pulp

# Data
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Extracting data
time = data['time']
profit = data['profit']
capacity = data['capacity']

# Number of parts and shops
K = len(profit)
S = len(capacity)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(profit[k] * quantity[k] for k in range(K)), "Total_Profit"

# Constraints
for s in range(S):
    problem += pulp.lpSum(time[k][s] * quantity[k] for k in range(K)) <= capacity[s], f"Capacity_Constraint_Shop_{s}"

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')