import pulp
import json

# Input data in JSON format
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'setup_time': [12, 8, 4, 0]}

# Extracting data from the input
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
setup_time = data['setup_time']

P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the problem instance
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')
setup_flags = pulp.LpVariable.dicts("setup_flags", range(P), cat='Binary')

# Objective function: Maximize profit
profit = pulp.lpSum([batches[p] * prices[p] for p in range(P)]) - \
         pulp.lpSum([batches[p] * (setup_flags[p] * setup_time[p] * machine_costs[0] + 
                                    pulp.lpSum([time_required[m][p] * machine_costs[m] for m in range(M)]) )
                      for p in range(P)])
problem += profit

# Constraints for machine availability 
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Setup time constraint applied only for machine 1
for p in range(P):
    problem += batches[p] <= setup_flags[p] * (availability[0] // setup_time[p])

# Solve the optimization problem
problem.solve()

# Prepare the output
batches_result = [int(batches[p].varValue) for p in range(P)]
setup_flags_result = [int(setup_flags[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output the results
output = {
    "batches": batches_result,
    "setup_flags": setup_flags_result,
    "total_profit": total_profit
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')