import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Parameters
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines
U = 100  # Assumed upper limit for batches to ensure correct setup_flags

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
setup_flags = [pulp.LpVariable(f'setup_flags_{p}', cat='Binary') for p in range(P)]

# Objective Function
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) \
         - pulp.lpSum([data['machine_costs'][m] * (
             pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) +
             (1 if m == 0 else 0) * pulp.lpSum([data['setup_time'][p] * setup_flags[p] for p in range(P)])
         ) for m in range(M)])

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) \
               + (1 if m == 0 else 0) * pulp.lpSum([data['setup_time'][p] * setup_flags[p] for p in range(P)]) \
               <= data['availability'][m]

for p in range(P):
    problem += setup_flags[p] >= batches[p] / U

# Solve
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')