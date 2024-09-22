import pulp
import json

# Given data in JSON format
data = json.loads("{'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'machine_costs': [160, 10, 15], 'availability': [200, 300, 500], 'prices': [570, 250, 585, 430], 'min_batches': [10, 10, 10, 10]}")

# Extracting data
time_required = data['time_required']  # time required for each part on each machine
machine_costs = data['machine_costs']   # cost associated with each machine
availability = data['availability']       # available time for each machine
prices = data['prices']                   # price for each part
min_batches = data['min_batches']         # minimum production requirements for each part

# Defining parameters
P = len(prices)  # number of parts
M = len(machine_costs)  # number of machines

# Creating the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables 
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum([prices[p] * x[p] for p in range(P)]) - pulp.lpSum([
    machine_costs[m] * pulp.lpSum([time_required[m][p] * x[p] for p in range(P)])
    for m in range(M)
])
problem += profit, "Total_Profit"

# Constraints
# Machine Availability
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * x[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Minimum Production Requirements
for p in range(P):
    problem += x[p] >= min_batches[p], f"Min_Production_{p}"

# Solving the problem
problem.solve()

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')