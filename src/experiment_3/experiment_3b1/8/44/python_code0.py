import pulp
import json

# Data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Parameters
P = len(data['prices'])  # Number of different parts
M = len(data['machine_costs'])  # Number of different machines
time_required = data['time_required']  # Time required on machines for each part
machine_costs = data['machine_costs']  # Costs per hour for machines
availability = data['availability']  # Available hours for each machine
prices = data['prices']  # Selling prices for each part
min_batches = data['min_batches']  # Minimum batches for each part

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')