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

# Problem Setup
P = len(data['prices'])
M = len(data['machine_costs'])
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Define the problem
problem = pulp.LpProblem("AutoPartsProduction", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective Function: Maximize total profit
total_profit = pulp.lpSum([(prices[p] * batches[p]) - 
                            (pulp.lpSum([(time_required[m][p] * batches[p]) * machine_costs[m] 
                                          for m in range(M)])) for p in range(P)])
problem += total_profit

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p]  # Minimum batch constraint

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m]

# Profit constraint
problem += total_profit >= min_profit

# Solve the problem
problem.solve()

# Output the results
result_batches = [int(batches[p].varValue) for p in range(P)]
total_profit_value = pulp.value(problem.objective)

output = {
    "batches": result_batches,
    "total_profit": total_profit_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit_value}</OBJ>')