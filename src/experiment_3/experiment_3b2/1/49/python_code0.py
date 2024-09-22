import pulp

# Data input from JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10]
}

# Extracting data
time_required = data['time_required']  # time_required[m][p]
machine_costs = data['machine_costs']  # cost for each machine
availability = data['availability']      # available time for each machine
prices = data['prices']                  # selling price for each part
min_batches = data['min_batches']        # minimum batches for each part

# Define the number of parts and machines
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints
# Machine Time Constraints
for m in range(M - 1):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Shared Availability for Machine M and Machine M-1
problem += pulp.lpSum([time_required[M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([time_required[M-2][p] * batches[p] for p in range(P)]) <= availability[M-1] + availability[M-2]

# Minimum Batch Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')