import pulp

# Data from JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P))
costs = pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P))
    for m in range(M)
)
problem += profit - costs, "Total_Profit"

# Constraints

# Availability constraints for Machines 1 to M-2
for m in range(M-2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m], f"Machine_{m+1}_Availability"

# Combined availability constraint for Machines M-1 and M
problem += pulp.lpSum(time_required[M-2][p] * x[p] for p in range(P)) + \
           pulp.lpSum(time_required[M-1][p] * x[p] for p in range(P)) <= availability[M-2] + availability[M-1], "Combined_Machines_Availability"

# Minimum production constraint for each part
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Production_{p+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')