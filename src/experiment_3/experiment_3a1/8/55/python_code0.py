import json
import pulp

# Data from the provided JSON format
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

# Number of parts and machines
P = len(data['prices'])
M = len(data['machine_costs'])

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
b = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Objective function
profit_expr = pulp.lpSum([data['prices'][p] * b[p] for p in range(P)]) - \
               pulp.lpSum([data['machine_costs'][m] * pulp.lpSum([data['time_required'][m][p] * b[p] for p in range(P)]) for m in range(M)]) 

# Calculate total_hours for labor costs
total_hours = pulp.lpSum([data['time_required'][0][p] * b[p] for p in range(P)])  # Hours from Machine 1
labor_costs = pulp.ifthen(total_hours <= data['overtime_hour'],
                          data['standard_cost'] * total_hours)
labor_costs += pulp.ifthen(total_hours > data['overtime_hour'],
                           data['standard_cost'] * data['overtime_hour'] +
                           data['overtime_cost'] * (total_hours - data['overtime_hour']))

# Add labor costs to the profit expression
profit_expr -= labor_costs

# Set the objective
problem += profit_expr, "Total_Profit"

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum([data['time_required[m][p]'] * b[p] for p in range(P)]) <= data['availability'][m], f"Availability_Constraint_{m+1}"

# Minimum Batch Production Constraints
for p in range(P):
    problem += b[p] >= data['min_batches'][p], f"Min_Batch_Constraint_{p+1}"

# Profit Constraints
problem += profit_expr >= data['min_profit'], "Profit_Constraint"

# Solve the problem
problem.solve()

# Output the results
batches = [b[p].varValue for p in range(P)]
total_profit = pulp.value(problem.objective)

print(f' (Batches Produced): {batches}')
print(f' (Total Profit): <OBJ>{total_profit}</OBJ>')