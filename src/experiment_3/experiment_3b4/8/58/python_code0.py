import pulp

# Data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'setup_time': [12, 8, 4, 0]
}

# Parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)
M = len(machine_costs)

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Integer') for p in range(P)]
y = [pulp.LpVariable(f'y_{p}', cat='Binary') for p in range(P)]

# Objective function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)])
costs = pulp.lpSum([
    machine_costs[m] * (
        pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) +
        (setup_time[p] * y[p] if m == 0 else 0)
    ) for m in range(M)
])

problem += profit - costs, "Total Profit"

# Constraints

# Machine availability constraints
for m in range(M):
    problem += (
        pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) +
        (pulp.lpSum([setup_time[p] * y[p] for p in range(P)]) if m == 0 else 0)
        <= availability[m]
    ), f"Machine Availability {m}"

# Setup flag constraint for machine 1
for p in range(P):
    problem += y[p] <= x[p], f"Setup Flag Constraint {p}"

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')