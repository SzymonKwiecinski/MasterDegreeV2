import pulp
import json

# Data provided in JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Parameters
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

# Decision Variables
batches = pulp.LpVariable.dicts("Batch", range(num_parts), lowBound=0, cat='Continuous')

# Objective Function
profit_expr = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) \
               - pulp.lpSum(machine_costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) for m in range(num_machines))

problem += profit_expr, "Total_Profit"

# Constraints
# Machine Availability Constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"Machine_Availability_{m+1}"

# Minimum Batches Requirement
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p+1}"

# Labor Cost Constraints on Machine 1
for p in range(num_parts):
    problem += time_required[0][p] * batches[p] <= availability[0], f"Labor_Cost_Machine1_{p+1}"

# Additional Overtime Constraints
for p in range(num_parts):
    problem += time_required[0][p] * batches[p] <= availability[0] + overtime_hour[0], f"Overtime_Cost_Machine1_{p+1}"

# Solve the problem
problem.solve()

# Output the results
batches_output = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

print(f'Batches: {batches_output}, Total Profit: {total_profit}')
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')