import pulp
import json

# Input data
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

# Extracting parameters
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) \
               - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(num_parts)) for m in range(num_machines))

# Add extra cost for machine 1 for labor
labor_expr = (
    pulp.lpSum((standard_cost * pulp.lpSum(time_required[0][p] * batches[p] for p in range(num_parts)) / 100)) +
                (overtime_cost * pulp.lpSum((time_required[0][p] * batches[p] / 100 - overtime_hour[0]) * (time_required[0][p] * batches[p] / 100 > overtime_hour[0]) for p in range(num_parts))) 
                for p in range(num_parts))
)

# Complete objective function
problem += profit_expr - labor_expr, "Total_Profit"

# Constraints
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] / 100 for p in range(num_parts)) <= availability[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Collect results
batches_result = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')