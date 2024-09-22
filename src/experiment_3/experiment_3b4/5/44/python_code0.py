import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

time_required = data['time_required']
cost_m = data['machine_costs']
available_m = data['availability']
price_p = data['prices']
min_batches_p = data['min_batches']

P = len(price_p)
M = len(cost_m)

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p+1}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
revenue = pulp.lpSum([price_p[p] * batches[p] for p in range(P)])
machine_costs = pulp.lpSum([cost_m[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += revenue - machine_costs, "Total Profit"

# Constraints
# Machine availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= available_m[m], f"Machine_Usage_{m+1}"

# Minimum batch requirements
for p in range(P):
    problem += batches[p] >= min_batches_p[p], f"Min_Batches_{p+1}"

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')