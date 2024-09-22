import pulp

# Data from the provided JSON
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting values from data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Defining parameters
P = len(prices)  # Number of parts
M = len(availability)  # Number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=min_batches[p], cat='Continuous') for p in range(P)]

# Objective function
profit = pulp.lpSum(prices[p] * x[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M))

problem += profit

# Constraints for machine time
for m in range(M - 2):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Shared availability for the last two machines
problem += pulp.lpSum(time_required[M - 2][p] * x[p] for p in range(P)) + \
           pulp.lpSum(time_required[M - 1][p] * x[p] for p in range(P)) <= availability[M - 2] + availability[M - 1]

# Minimum production requirements
for p in range(P):
    problem += x[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')