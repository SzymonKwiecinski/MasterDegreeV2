import pulp

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10], 'extra_costs': [0, 15, 22.5], 'max_extra': [0, 80, 80]}

# Extract the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

M = len(machine_costs)  # Number of machines
P = len(prices)         # Number of parts

# Define the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', min_batches[p], cat='Continuous') for p in range(P)]
extra_time = [pulp.LpVariable(f'extra_time_{m}', 0, max_extra[m], cat='Continuous') for m in range(M)]

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) \
         - pulp.lpSum((machine_costs[m] * availability[m] + extra_costs[m] * extra_time[m]) for m in range(M)) \
         - pulp.lpSum(machine_costs[m] * time_required[m][p] * batches[p] for m in range(M) for p in range(P))

problem += profit, "Total Profit"

# Constraints
for m in range(M):
    problem += (
        pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m] + extra_time[m], 
        f"Machine_{m}_Time_Constraint"
    )

# Solve the problem
problem.solve()

# Output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "extra_time": [pulp.value(extra_time[m]) for m in range(M)],
    "total_profit": pulp.value(problem.objective)
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')