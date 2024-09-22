import pulp
import json

# Data provided
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10], "extra_costs": [0, 15, 22.5], "max_extra": [0, 80, 80]}')

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
extra_costs = data['extra_costs']
max_extra = data['max_extra']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Define the Linear Programming problem
problem = pulp.LpProblem("AutoPartsManufacturing", pulp.LpMaximize)

# Decision Variables
b = pulp.LpVariable.dicts("b", range(P), lowBound=0)  # Batches produced for each part
e = pulp.LpVariable.dicts("e", range(M), lowBound=0)  # Extra hours for each machine

# Objective Function
profit = pulp.lpSum(prices[p] * b[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * (pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) + e[m]) + extra_costs[m] * e[m] for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Time availability constraints for each machine
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * b[p] for p in range(P)) + e[m] <= availability[m] + max_extra[m], f"Time_Availability_Constraint_{m}"

# Minimum production requirements for each part
for p in range(P):
    problem += b[p] >= min_batches[p], f"Min_Production_Requirement_Constraint_{p}"

# Solve the problem
problem.solve()

# Output Results
produced_batches = [b[p].varValue for p in range(P)]
extra_hours = [e[m].varValue for m in range(M)]

print(f'Produced batches: {produced_batches}')
print(f'Extra hours purchased: {extra_hours}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')