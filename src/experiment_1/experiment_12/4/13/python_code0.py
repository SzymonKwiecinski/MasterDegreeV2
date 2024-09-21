import pulp

# Data from JSON
data = {
    'time': [[2, 3], [1, 2], [3, 2], [3, 1], [1, 1]], 
    'profit': [30, 20, 40, 25, 10], 
    'capacity': [700, 1000]
}

time = data['time']
profit = data['profit']
capacity = data['capacity']

K = len(profit)  # Number of spare parts
S = len(capacity)  # Number of machines

# Create a Linear Programming problem
problem = pulp.LpProblem("Optimal_Production_Spare_Parts", pulp.LpMaximize)

# Decision Variables: x_k is the quantity of spare part k to produce
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function: Maximize total profit
problem += pulp.lpSum([profit[k] * x[k] for k in range(K)])

# Constraints

# Machine capacity constraints
for s in range(S):
    problem += pulp.lpSum([time[k][s] * x[k] for k in range(K)]) <= capacity[s]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')