import pulp

# Parse the JSON data
data = {
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "extra_costs": [0, 15, 22.5],
    "max_extra": [0, 80, 80]
}

# Number of parts and machines
P = len(data["prices"])
M = len(data["machine_costs"])

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data["min_batches"][p], cat='Integer') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data["max_extra"][m], cat='Continuous') for m in range(M)]

# Objective function
total_revenue = pulp.lpSum([data["prices"][p] * batches[p] for p in range(P)])
total_machine_cost = pulp.lpSum([data["machine_costs"][m] * (data["availability"][m] + extra_time[m]) for m in range(M)])
total_extra_cost = pulp.lpSum([data["extra_costs"][m] * extra_time[m] for m in range(M)])

problem += total_revenue - total_machine_cost - total_extra_cost

# Constraints
for m in range(M):
    problem += pulp.lpSum([data["time_required"][m][p] * batches[p] for p in range(P)]) <= data["availability"][m] + extra_time[m]

# Solve
problem.solve()

# Extract results
solution = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "extra_time": [pulp.value(extra_time[m]) for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')