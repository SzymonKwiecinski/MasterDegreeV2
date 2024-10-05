import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Sets
M = range(len(data['machine_costs']))  # Machines
P = range(len(data['prices']))         # Parts

# Decision Variables
batches = pulp.LpVariable.dicts("batches", P, lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in P)
machine_costs = pulp.lpSum(data['machine_costs'][m] * 
                           pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P)
                           for m in M)
problem += profit - machine_costs

# Constraints
# Machine availability constraints
for m in M:
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in P) <= data['availability'][m], f"Machine_avail_{m}"

# Minimum production requirement for each part
for p in P:
    problem += batches[p] >= data['min_batches'][p], f"Min_batches_{p}"

# Solve
problem.solve()

# Results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')