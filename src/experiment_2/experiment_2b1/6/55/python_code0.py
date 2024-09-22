import pulp
import json

data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Extracting information from the data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Number of parts and machines
P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Integer')

# Objective function: Total profit
profit = pulp.lpSum([(prices[p] * batches[p]) for p in range(P)])
costs = pulp.lpSum([(machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)])) for m in range(M)])
labor_cost = (standard_cost * pulp.lpSum([pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]))
problem += profit - costs - labor_cost, "Total_Profit"

# Constraints
# Time constraints for each machine
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_Machine_{m}"

# Minimum batches for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Minimum_Batches_Constraint_Part_{p}"

# Profit constraint
problem += profit - costs - labor_cost >= min_profit, "Minimum_Profit_Constraint"

# Solve the problem
problem.solve()

# Collecting results
result_batches = [batches[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "batches": result_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')