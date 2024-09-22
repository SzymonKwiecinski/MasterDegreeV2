import pulp
import json

# Input data
data = {'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'machine_costs': [160, 10, 15], 
        'availability': [200, 300, 500], 
        'prices': [570, 250, 585, 430], 
        'min_batches': [10, 10, 10, 10], 
        'standard_cost': 20, 
        'overtime_cost': 30, 
        'overtime_hour': 400, 
        'min_profit': 5000}

# Extracting data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

P = len(prices)
M = len(machine_costs)

# Create the problem
problem = pulp.LpProblem("Auto_Parts_Production", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Total profit
total_profit = pulp.lpSum((prices[p] - (pulp.lpSum([time_required[m][p] * batches[p] * machine_costs[m] for m in range(M)])) / 100) for p in range(P)))
problem += total_profit, "Total_Profit"

# Constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_Constraint_{m}"

for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p}"

# Profit constraint
problem += total_profit >= min_profit, "Min_Profit_Constraint"

# Solve the problem
problem.solve()

# Extract results
batches_solution = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output results
output = {
    "batches": batches_solution,
    "total_profit": total_profit_value
}

print(f' (Objective Value): <OBJ>{output["total_profit"]}</OBJ>')