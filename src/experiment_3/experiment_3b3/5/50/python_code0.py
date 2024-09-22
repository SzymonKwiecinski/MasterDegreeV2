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

P = len(data['min_batches'])
M = len(data['machine_costs'])

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, cat='Continuous') for m in range(M)]

# Objective Function
total_profit = (
    pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) 
    - pulp.lpSum(data['machine_costs'][m] * (data['availability'][m] + extra_time[m]) for m in range(M))
    - pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))
)
problem += total_profit

# Constraints
# Production Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m] + extra_time[m]

# Extra Time Purchase Constraints
for m in range(M):
    problem += extra_time[m] <= data['max_extra'][m]

# Solve the problem
problem.solve()

# Output
print("Batches produced for each part:")
for p in range(P):
    print(f"Part {p + 1}: {batches[p].varValue}")

print("\nExtra time purchased for each machine:")
for m in range(M):
    print(f"Machine {m + 1}: {extra_time[m].varValue}")

print(f"\nTotal Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")