import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
P = len(data['prices'])  # number of parts
M = len(data['time_required'])  # number of machines
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum((data['prices'][p] * batches[p] - pulp.lpSum(data['time_required[m][p]'] * data['machine_costs'][m] * (batches[p] // 100) for m in range(M)) for p in range(P)))
problem += profit, "Total_Profit"

# Constraints
for p in range(P):
    problem += batches[p] >= data['min_batches'][p], f"MinBatches_part_{p}"
    
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m], f"Availability_machine_{m}"

# Solve the problem
problem.solve()

# Output the results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')