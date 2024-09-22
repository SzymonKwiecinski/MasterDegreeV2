import pulp
import json

# Input data
data = {
    'time_required': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
    'machine_costs': [160, 10, 15], 
    'availability': [200, 300, 500], 
    'prices': [570, 250, 585, 430], 
    'min_batches': [10, 10, 10, 10], 
    'standard_cost': 20, 
    'overtime_cost': 30, 
    'overtime_hour': 400, 
    'min_profit': 5000
}

# Extract data
time_required = data['time_required']
machine_costs = data['machine_costs']
availability = data['availability']
prices = data['prices']
min_batches = data['min_batches']
standard_cost = data['standard_cost']
overtime_cost = data['overtime_cost']
overtime_hour = data['overtime_hour']
min_profit = data['min_profit']

# Problem variables
P = len(prices)
M = len(machine_costs)

# Define the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
total_profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) - pulp.lpSum(
    (pulp.lpSum(time_required[m][p] * machine_costs[m] * batches[p] for p in range(P)) for m in range(M))
)

problem += total_profit

# Constraints for minimum production
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Constraints for machine availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# Calculate labor costs for Machine 1
labor_cost = pulp.lpSum(batches[p] * time_required[0][p] for p in range(P))
problem += labor_cost <= (overtime_hour * standard_cost) + (overtime_cost * (labor_cost - overtime_hour)) * (labor_cost > overtime_hour)

# Ensuring minimum profit is achieved
problem += total_profit >= min_profit

# Solve the problem
problem.solve()

# Collect results
result_batches = [batches[p].varValue for p in range(P)]
total_profit_value = pulp.value(problem.objective)

# Output formatting
output = {
    "batches": result_batches,
    "total_profit": total_profit_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')