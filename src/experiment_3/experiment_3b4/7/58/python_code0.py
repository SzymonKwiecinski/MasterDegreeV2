import pulp

# Data provided
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'setup_time': [12, 8, 4, 0]
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Number of parts and machines
num_parts = len(prices)
num_machines = len(machine_costs)

# Create a Linear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(num_parts)]
y = [pulp.LpVariable(f'y_{p}', cat='Binary') for p in range(num_parts)]

# Objective function
revenue = pulp.lpSum(prices[p] * x[p] for p in range(num_parts))
costs = pulp.lpSum(machine_costs[m] * (
    pulp.lpSum(time_required[m][p] * x[p] for p in range(num_parts)) +
    (setup_time[p] * y[p] if m == 0 else 0)
) for m in range(num_machines))

problem += revenue - costs

# Constraints
for m in range(num_machines):
    constraint = pulp.lpSum(time_required[m][p] * x[p] for p in range(num_parts))
    if m == 0:
        constraint += pulp.lpSum(setup_time[p] * y[p] for p in range(num_parts))
    problem += constraint <= availability[m]

for p in range(num_parts):
    problem += y[p] >= x[p] / num_machines

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')