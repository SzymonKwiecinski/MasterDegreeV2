import pulp

# Data from the JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem
problem = pulp.LpProblem("AutoPartsProfitMaximization", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function: Maximize total profit
profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)])
costs = pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - costs, "Total Profit"

# Constraints

# Machine time availability constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m], f"Machine_{m}_Time_Availability"

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output: Decision Variables and Objective Value
for p in range(P):
    print(f'Batches of part {p}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')