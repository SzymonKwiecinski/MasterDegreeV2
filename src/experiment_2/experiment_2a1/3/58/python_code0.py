import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Data unpacking
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

P = len(prices)
M = len(machine_costs)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function
profit = pulp.lpSum((prices[p] - pulp.lpSum(time_required[m][p] * machine_costs[m] for m in range(M))) * batches[p] for p in range(P))
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]
    
# Setup time constraints for machine 1
for p in range(P):
    problem += batches[p] <= setup_flags[p] * (availability[0] / (time_required[0][p] if time_required[0][p] != 0 else 1))

# Solve the problem
problem.solve()

# Collecting results
batches_result = [batches[p].varValue for p in range(P)]
setup_flags_result = [setup_flags[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')