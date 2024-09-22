import pulp
import json

# Input data in JSON format
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

# Problem definition
P = len(prices)  # Number of parts
M = len(machine_costs)  # Number of machines

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize total profit
total_profit = pulp.lpSum((prices[p] * batches[p] - 
                            pulp.lpSum((time_required[m][p] * machine_costs[m] / 100) * batches[p] 
                                        for m in range(M))) for p in range(P))
problem += total_profit

# Constraints
# Machine availability constraints
for m in range(M):
    problem += (pulp.lpSum((time_required[m][p] * batches[p]) for p in range(P)) <= availability[m], 
                           f"Availability_Constraint_Machine_{m}")

# Minimum production constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Batches_Constraint_Part_{p}")

# Shared availability constraints for Machine M and M-1
if M > 1:
    problem += (pulp.lpSum((time_required[M-1][p] * batches[p]) for p in range(P)) + 
                      pulp.lpSum((time_required[M-2][p] * batches[p]) for p in range(P)) 
                      <= availability[M-1] + availability[M-2], 
                      f"Shared_Availability_Constraint_M{M-1}_and_M{M}")

# Solve the problem
problem.solve()

# Prepare output
batches_output = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Final output in specified format
output = {
    "batches": batches_output,
    "total_profit": total_profit_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')