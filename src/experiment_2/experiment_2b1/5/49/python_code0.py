import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10]}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines
# Combine availability of machine M and M-1
total_availability = sum(availability[-2:]) if M > 1 else availability[0]

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
problem += pulp.lpSum((prices[p] * batches[p] - 
                        pulp.lpSum(time_required[m][p] * machine_costs[m] * (batches[p] // 100) 
                                   for m in range(M))) 
                       for p in range(P)), "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

# Minimum batches constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Outputting results
batches_produced = [int(batches[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')