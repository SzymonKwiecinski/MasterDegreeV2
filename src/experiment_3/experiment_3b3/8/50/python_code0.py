import pulp

# Data provided in JSON format
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
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'batch_{p}', lowBound=0, cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(M)]

# Objective Function
profit = (
    pulp.lpSum([prices[p] * batches[p] for p in range(P)]) -
    pulp.lpSum([machine_costs[m] * (availability[m] + extra_time[m]) for m in range(M)]) -
    pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(M)])
)
problem += profit

# Constraints

# Machine time constraints
for m in range(M):
    problem += (
        pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m] + extra_time[m]
    )

# Minimum production requirements
for p in range(P):
    problem += (batches[p] >= min_batches[p])

# Solve problem
problem.solve()

# Output
batches_solution = [batches[p].varValue for p in range(P)]
extra_time_solution = [extra_time[m].varValue for m in range(M)]

print(f"Batches Produced: {batches_solution}")
print(f"Extra Time Purchased: {extra_time_solution}")
print(f"Total Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")