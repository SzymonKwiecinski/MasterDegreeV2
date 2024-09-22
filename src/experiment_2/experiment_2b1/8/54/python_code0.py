import json
import pulp

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

# Create the problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches to produce for each part
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Integer')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     (pulp.lpSum((time_required[m][p] * batches[p] / 100) * machine_costs[m] for m in range(num_machines))) +
                     (pulp.lpSum((time_required[0][p] * batches[p] / 100) * standard_cost for p in range(num_parts)) if batches[p] > 0 else 0) +
                     (pulp.lpSum(((time_required[0][p] * batches[p] / 100) - overtime_hour[i]) * overtime_cost for i in range(num_parts) if (time_required[0][p] * batches[p] / 100) > overtime_hour[i])))))
                  for p in range(num_parts))

problem += profit

# Constraints for minimum batches
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Constraints for machine availability
for m in range(num_machines):
    problem += pulp.lpSum((time_required[m][p] * batches[p] / 100) for p in range(num_parts)) <= availability[m], f"Availability_{m}"

# Solve the problem
problem.solve()

# Output result
batches_result = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Print results
print(json.dumps({
    "batches": batches_result,
    "total_profit": total_profit
}, indent=4))

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')