import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Unpack data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Constants
P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) for m in range(M)
)

# Constraints
# Non-negativity and minimum production requirement constraint
for p in range(P):
    problem += x[p] >= min_batches[p]

# Machine time availability constraint
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')