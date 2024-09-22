import pulp

# Parse the data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10],
    'extra_costs': [0, 15, 22.5],
    'max_extra': [0, 80, 80]
}

time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
num_parts = len(prices)
num_machines = len(machine_costs)

batches = [pulp.LpVariable(f'b_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(num_parts)]
extra_time = [pulp.LpVariable(f'e_{m}', lowBound=0, upBound=max_extra[m], cat='Continuous') for m in range(num_machines)]

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)]) - \
         pulp.lpSum([machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) + extra_time[m]) for m in range(num_machines)]) - \
         pulp.lpSum([extra_costs[m] * extra_time[m] for m in range(num_machines)])

problem += profit

# Constraints
# Machine time constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m] + extra_time[m]

# Solve
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')