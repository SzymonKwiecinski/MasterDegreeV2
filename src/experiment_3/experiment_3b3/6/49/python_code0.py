import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Problem definition
problem = pulp.LpProblem("AutoParts_Manufacturer", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective function
total_profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
               pulp.lpSum(data['machine_costs'][m] * pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) for m in range(M))

problem += total_profit

# Constraints
# Machine time constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Shared availability constraint for machines M-1 and M
problem += (pulp.lpSum(data['time_required'][M-1][p] * batches[p] for p in range(P)) +
            pulp.lpSum(data['time_required'][M-2][p] * batches[p] for p in range(P))) <= \
           (data['availability'][M-1] + data['availability'][M-2])

# Minimum production requirement for each part
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Solving the problem
problem.solve()

# Output the solution
batches_output = [pulp.value(batches[p]) for p in range(P)]
total_profit_output = pulp.value(problem.objective)

print(f"(Objective Value): <OBJ>{total_profit_output}</OBJ>")