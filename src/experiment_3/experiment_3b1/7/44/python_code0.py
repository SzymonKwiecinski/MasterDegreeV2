import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracted Data
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']   # cost_m
availability = data['availability']       # available_m
prices = data['prices']                   # price_p
min_batches = data['min_batches']         # min_batches_p

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
P = len(prices)  # Number of parts
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) for m in range(len(machine_costs)))

problem += profit

# Constraints
# Machine availability constraints
for m in range(len(availability)):
    problem += (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) <= availability[m]), f"Availability_Constraint_{m}"

# Minimum production requirements
for p in range(P):
    problem += (b[p] >= min_batches[p]), f"Min_Batch_Constraint_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')