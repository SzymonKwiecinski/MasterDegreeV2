import pulp

# Data
data = {
    'time_required': [
        [2, 1, 3, 2],
        [4, 2, 1, 2],
        [6, 2, 1, 2]
    ],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}
epsilon = 0.001  # very small positive epsilon to ensure y_p is binary

# Parameters
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Integer') for p in range(P)]
y = [pulp.LpVariable(f'y_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([data['prices'][p] * x[p] for p in range(P)]) \
         - pulp.lpSum([pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) * data['machine_costs'][m] for m in range(M)]) \
         - pulp.lpSum([data['setup_time'][p] * y[p] * data['machine_costs'][0] for p in range(P)])

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * x[p] for p in range(P)]) \
               + (data['setup_time'][p] * y[p] if m == 0 else 0) <= data['availability'][m]

for p in range(P):
    problem += y[p] >= x[p] / (1 + epsilon)

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')