import pulp

# Parse input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

# Decision variables for batches
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data["min_batches"][p], cat='Continuous') for p in range(len(data["prices"]))]
# Decision variables for extra time
extra_time = [pulp.LpVariable(f'extra_time_{m}', lowBound=0, upBound=data["max_extra"][m], cat='Continuous') for m in range(len(data["machine_costs"]))]

# Initialize the problem
problem = pulp.LpProblem("Profit_Maximization_Problem", pulp.LpMaximize)

# Objective function
revenue = pulp.lpSum(batches[p] * data["prices"][p] for p in range(len(data["prices"])))
costs = pulp.lpSum(extra_time[m] * data["extra_costs"][m] for m in range(len(data["extra_costs"]))) + \
        pulp.lpSum((pulp.lpSum(data["time_required"][m][p] * batches[p] for p in range(len(data["prices"]))) * data["machine_costs"][m]) for m in range(len(data["machine_costs"])))
profit = revenue - costs

problem += profit

# Constraints for machine hour availability
for m in range(len(data["availability"])):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(len(data["prices"]))) <= \
               data['availability'][m] + extra_time[m]

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "batches": [pulp.value(batches[p]) for p in range(len(data["prices"]))],
    "extra_time": [pulp.value(extra_time[m]) for m in range(len(data["machine_costs"]))],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')