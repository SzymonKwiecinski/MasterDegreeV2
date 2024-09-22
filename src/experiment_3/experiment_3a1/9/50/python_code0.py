import pulp
import json

# Data
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Parameters
P = len(data['prices'])
M = len(data['machine_costs'])
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)  # number of batches for each part
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)  # additional hours

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
    pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m]) for m in range(M)) - \
    pulp.lpSum(extra_costs[m] * extra_time[m] for m in range(M))

problem += profit

# Constraints

# Machine Availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) + extra_time[m] <= availability[m] + max_extra[m], f"Availability_Constraint_{m}"

# Minimum Production Requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Production_Constraint_{p}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')