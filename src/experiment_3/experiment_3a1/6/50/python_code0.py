import pulp
import json

# Input data
data = """
{
    "time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "machine_costs": [160, 10, 15],
    "availability": [200, 300, 500],
    "prices": [570, 250, 585, 430],
    "min_batches": [10, 10, 10, 10],
    "extra_costs": [0, 15, 22.5],
    "max_extra": [0, 80, 80]
}
"""
data = json.loads(data)

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

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)
extra_time = pulp.LpVariable.dicts("extra_time", range(M), lowBound=0)

# Create the problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Objective Function
total_profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
    pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + extra_costs[m] * extra_time[m] for m in range(M)])

problem += total_profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) + extra_time[m] <= 
                 availability[m] + max_extra[m]), f"MachineTimeConstraint_{m}")

for p in range(P):
    problem += (batches[p] >= min_batches[p]), f"MinBatchesConstraint_{p}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')