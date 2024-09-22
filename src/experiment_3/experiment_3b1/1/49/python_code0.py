import pulp

# Data from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Define the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Define sets
P = len(data['prices'])  # Number of parts
M = len(data['machine_costs'])  # Number of machines

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)  # Batches for each part

# Objective function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_constraint_{m}"

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_batches_constraint_{p}"

# Solve the problem
problem.solve()

# Output the results
batches_values = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches produced: {batches_values}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')