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

# Problem formulation
P = len(data['prices'])  # number of parts
M = len(data['machine_costs'])  # number of machines

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum((data['prices'][p] * batches[p] - 
                     pulp.lpSum(data['time_required'][m][p] * data['machine_costs'][m] * batches[p] / 100 
                     for m in range(M)) for p in range(P))
                     )

problem += profit

# Constraints
# Minimum production requirements
for p in range(P):
    problem += batches[p] >= data['min_batches'][p]

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) <= data['availability'][m]

# Solve the problem
problem.solve()

# Extract results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')