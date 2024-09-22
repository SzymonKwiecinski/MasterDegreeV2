import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Indices
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective Function
profit_from_batches = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))

cost_of_machines = pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M))
extra_time_cost = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))

problem += profit_from_batches - cost_of_machines - extra_time_cost

# Constraints

# Production Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Extra time constraints
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Output results
batches_produced = {f'part_{p}': batches[p].varValue for p in range(P)}
extra_time_purchased = {f'machine_{m}': extra_time[m].varValue for m in range(M)}
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_produced}')
print(f'Extra Time Purchased: {extra_time_purchased}')
print(f'Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')