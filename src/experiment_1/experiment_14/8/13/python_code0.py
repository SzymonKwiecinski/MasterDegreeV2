import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]],
    'profit': [30, 20, 40, 25, 10],
    'capacity': [700, 1000]
}

# Number of different spare parts (K)
K = len(data['profit'])

# Number of machines (S)
S = len(data['capacity'])

# Time matrix
Time = data['time']

# Profit list
Profit = data['profit']

# Capacity list
Capacity = data['capacity']

# Define the Linear Programming problem
problem = pulp.LpProblem("Spare_Parts_Production", pulp.LpMaximize)

# Decision Variables: Quantity of each spare part to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Maximize total profit
problem += pulp.lpSum(Profit[k] * x[k] for k in range(K)), "Total_Profit"

# Constraints
# Time constraints for each machine
for s in range(S):
    problem += pulp.lpSum(Time[k][s] * x[k] for k in range(K)) <= Capacity[s], f"Capacity_Machine_{s+1}"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for k in range(K):
    print(f'Quantity of Spare Part {k+1}: {pulp.value(x[k])}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')