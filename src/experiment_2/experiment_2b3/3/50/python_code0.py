import pulp

# Data from the given JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Variables to represent sets
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data['max_extra'][m], cat='Continuous') for m in range(M)]

# Create a LP Maximization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective function: Maximize total profit
revenue = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P))
machine_cost = pulp.lpSum((data['machine_costs'][m] * (data['availability'][m] + extra_time[m])) for m in range(M))
extra_cost = pulp.lpSum(data['extra_costs'][m] * extra_time[m] for m in range(M))
problem += revenue - machine_cost - extra_cost

# Subject to time constraints for each machine
for m in range(M):
    total_time_on_machine = pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P))
    problem += total_time_on_machine <= data['availability'][m] + extra_time[m]

# Solve the problem
problem.solve()

# Output results
output = {
    "batches": [batches[p].varValue for p in range(P)],
    "extra_time": [extra_time[m].varValue for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')