import pulp
import json

data = {'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}

# Extracting data from JSON format
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function: Total profit
profit = pulp.lpSum([prices[p] * batches[p] for p in range(num_parts)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] / 100 for p in range(num_parts)]) for m in range(num_machines)]) - \
         pulp.lpSum([
             standard_cost * pulp.lpSum([batches[p] for p in range(num_parts) if time_required[0][p] * batches[p] <= overtime_hour[0]]) +
             overtime_cost * pulp.lpSum([batches[p] for p in range(num_parts) if time_required[0][p] * batches[p] > overtime_hour[0]])
         ])
         
problem += profit

# Constraints

# Minimum batches for each part
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Machine availability constraints
for m in range(num_machines):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(num_parts)]) <= availability[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Output results
batches_output = [int(batches[p].varValue) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
result = {
    "batches": batches_output,
    "total_profit": total_profit
}