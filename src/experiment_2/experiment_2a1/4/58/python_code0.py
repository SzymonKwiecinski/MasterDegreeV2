import pulp
import json

# Given data in JSON format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Problem parameters
M = len(data['machine_costs'])  # Number of machines
P = len(data['prices'])          # Number of parts

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective Function
profit = pulp.lpSum(data['prices'][p] * batches[p] for p in range(P)) - \
         pulp.lpSum(data['machine_costs'][m] * 
                     (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) + 
                     (data['setup_time'][p] * setup_flags[p] for p in range(P))) * (1 / 100) 
                     for m in range(M)))
problem += profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum(data['time_required'][m][p] * batches[p] for p in range(P)) +
                 pulp.lpSum(data['setup_time'][p] * setup_flags[p] for p in range(P))) <= data['availability'][m]

# Linking setup flags to batches
for p in range(P):
    problem += batches[p] <= 1000 * setup_flags[p]  # if batches[p] > 0, setup_flags[p] must be 1

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "batches": [pulp.value(batches[p]) for p in range(P)],
    "setup_flags": [pulp.value(setup_flags[p]) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')