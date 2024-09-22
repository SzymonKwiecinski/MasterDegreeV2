import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Constants
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Problem
problem = pulp.LpProblem("Maximize_Profit_Auto_Parts", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data['max_extra'][m], cat='Continuous') for m in range(M)]

# Objective Function
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_costs = pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))
extra_time_costs = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))
profit = revenue - machine_costs - extra_time_costs

problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Solve the problem
problem.solve()

# Output Results
print(f'Optimal Value (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')