import pulp
import json

data = {'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 
        'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 
        'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 
        'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}

# Extract parameters from the data
num_machines = data['NumMachines']
num_parts = data['NumParts']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hours = data['OvertimeHour']

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for the number of batches produced for each part
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Integer')

# Objective Function: Maximize profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * batches[p] * machine_costs[m]) / 100 
                                 for m in range(num_machines))) for p in range(num_parts))

problem += profit

# Constraints for machine availability
for m in range(num_machines):
    problem += pulp.lpSum((time_required[m][p] * batches[p]) for p in range(num_parts)) <= availability[m]

# Constraints for minimum batches
for p in range(num_parts):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Prepare output
batches_output = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output result
output = {
    "batches": batches_output,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')