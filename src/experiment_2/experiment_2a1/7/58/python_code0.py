import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Problem parameters
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

M = len(machine_costs)  # number of machines
P = len(prices)         # number of parts

# Create LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize profit
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - \
         pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) / 100 for m in range(M))
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_{m}_availability"

# Setup time constraints for machine 1
for p in range(P):
    if p == 0:  # Only the first part requires setup on machine 1
        problem += setup_flags[p] * setup_time[p] <= availability[0], f"Setup_time_part_{p}"

# Solving the problem
problem.solve()

# Output result
result = {
    "batches": [int(batches[p].varValue) for p in range(P)],
    "setup_flags": [int(setup_flags[p].varValue) for p in range(P)],
    "total_profit": pulp.value(problem.objective)
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')