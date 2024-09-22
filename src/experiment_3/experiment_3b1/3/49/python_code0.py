import pulp
import json

# Data provided in JSON format
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'machine_costs': [160, 10, 15],
    'availability': [200, 300, 500],
    'prices': [570, 250, 585, 430],
    'min_batches': [10, 10, 10, 10]
}

# Extracting data from JSON
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

# Defining the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Defining decision variables
P = len(prices)  # Number of parts
batches = pulp.LpVariable.dicts("b", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(len(machine_costs)))

problem += profit, "Total_Profit"

# Constraints
M = len(machine_costs)  # Number of machines
for m in range(M):
    if m == M - 1:  # Handle the last machine sharing with second to last
        problem += (pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) +
                     pulp.lpSum(time_required[m-1][p] * batches[p] for p in range(P))) <= availability[m] + availability[m-1], f"Time_Availability_{m}")
    else:
        problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Time_Availability_{m}")

# Minimum production requirements
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Output results
batches_produced = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f'Batches Produced: {batches_produced}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')