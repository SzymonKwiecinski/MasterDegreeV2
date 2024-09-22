import pulp
import json

# Data from the JSON format
data = json.loads('{"time_required": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "machine_costs": [160, 10, 15], "availability": [200, 300, 500], "prices": [570, 250, 585, 430], "min_batches": [10, 10, 10, 10]}')

# Initialize model
problem = pulp.LpProblem("Auto_Parts_Manufacturer", pulp.LpMaximize)

# Sets
P = len(data['prices'])       # Number of different parts
M = len(data['machine_costs']) # Number of different machines

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective Function
total_profit = pulp.lpSum([data['prices'][p] * batches[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += total_profit, "Total Profit"

# Constraints - Machine Availability
for m in range(M):
    problem += pulp.lpSum([data['time_required'][m][p] * batches[p] for p in range(P)]) <= data['availability'][m], f"Machine_Availability_Constraint_{m}"

# Shared Availability for M and M-1
problem += pulp.lpSum([data['time_required'][M-1][p] * batches[p] for p in range(P)]) + \
           pulp.lpSum([data['time_required'][M-2][p] * batches[p] for p in range(P)]) <= data['availability'][M-1] + data['availability'][M-2], "Shared_Availability_Constraint"

# Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"Min_Production_Requirement_{p}"

# Solve the problem
problem.solve()

# Output results
batches_produced = {f'Part_{p + 1}': batches[p].varValue for p in range(P)}
total_profit_value = pulp.value(problem.objective)
print(f'Batches produced: {batches_produced}')
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')