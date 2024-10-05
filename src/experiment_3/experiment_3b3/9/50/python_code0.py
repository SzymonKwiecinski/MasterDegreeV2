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

# Parameters
P = len(data['prices'])  # number of parts
M = len(data['availability'])  # number of machines

# Create a problem instance
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0, cat='Continuous')

# Objective Function
profit_terms = [
    data['prices'][p] * batches[p]
    - sum(data['machine_costs'][m] * (data['time_required'][m][p] / 100) * batches[p] for m in range(M))
    - sum(data['extra_costs'][m] * extra_time[m] for m in range(M)) for p in range(P)
]

problem += pulp.lpSum(profit_terms)

# Constraints

# Machine Time Availability Constraints
for m in range(M):
    problem += (
        pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
        <= data['availability'][m] + extra_time[m], f"Machine_Time_Constraint_{m}"
    )

# Minimum Batch Production Constraints
for p in range(P):
    problem += (batches[p] >= data['min_batches'][p], f"Min_Batches_Constraint_{p}")

# Maximum Extra Time Constraints
for m in range(M):
    problem += (extra_time[m] <= data['max_extra'][m], f"Max_Extra_Time_Constraint_{m}")

# Solve the problem
problem.solve()

# Printing results
print("Batches produced for each part:")
for p in range(P):
    print(f" - Part {p + 1}: {batches[p].varValue}")

print("Extra time purchased for each machine:")
for m in range(M):
    print(f" - Machine {m + 1}: {extra_time[m].varValue}")

print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")