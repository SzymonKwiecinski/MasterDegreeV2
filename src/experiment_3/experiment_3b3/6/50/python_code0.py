import pulp

# Define the data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision Variables
P = len(data['prices'])
M = len(data['availability'])
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, cat='Continuous') for m in range(M)]

# Objective Function
total_profit = (
    pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - 
    pulp.lpSum([data['machine_costs'][m] * (pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + 
                                              extra_time[m] * data['extra_costs'][m])
                for m in range(M)])
)
problem += total_profit

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += (
        pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) + extra_time[m] 
        <= data['availability'][m] + data['max_extra'][m],
        f"Machine_Availability_{m}"
    )

# Minimum Production Requirements
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Production_{p}")

# Solve the problem
problem.solve()

# Print the result
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')