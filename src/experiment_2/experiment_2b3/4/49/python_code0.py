import pulp

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

M = len(availability)
P = len(prices)

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function: Maximize total profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])
cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit - cost, "Total_Profit"

# Constraints
# Machine time availability (considering shared availability for machine M and M-1)
for m in range(M-1):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_{m+1}_Availability"

# Combined availability constraint for last two machines
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1], "Machine_M_And_M-1_Combined_Availability"

# Solve the problem
problem.solve()

# Output results
batches_result = [pulp.value(batches[p]) for p in range(P)]
total_profit = pulp.value(profit - cost)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(f'result: {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')