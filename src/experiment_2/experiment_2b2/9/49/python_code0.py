from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Number of machines (M) and parts (P)
M = len(data['time_required'])
P = len(data['time_required'][0])

# Defining the optimization problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables: number of batches produced for each part
batches = [LpVariable(f'batches_{p}', lowBound=data['min_batches'][p], cat='Integer') for p in range(P)]

# Objective function: maximize profit
profit = lpSum(data['prices'][p] * batches[p] for p in range(P))
costs = lpSum(data['time_required'][m][p] * data['machine_costs'][m] * batches[p] 
              for m in range(M) for p in range(P))
problem += profit - costs

# Constraints
for m in range(M - 1):
    problem += lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Combined constraint for the last two machines
problem += (lpSum(data['time_required'][M-1][p] * batches[p] for p in range(P)) +
            lpSum(data['time_required'][M-2][p] * batches[p] for p in range(P))) <= data['availability'][M-1]

# Solve the problem
problem.solve()

# Output the results
batches_solution = [value(batches[p]) for p in range(P)]
total_profit = value(profit - costs)

output = {
    "batches": batches_solution,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')