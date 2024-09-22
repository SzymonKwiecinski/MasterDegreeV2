import json
import pulp

# Data input
data = {'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}

# Variables
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
         pulp.lpSum(pulp.lpSum(time_required[m][p] * batches[p] * machine_costs[m] for p in range(num_parts)) for m in range(num_machines))

# Add the objective to the problem
problem += profit

# Constraints for minimum batches
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"MinBatches_Constraint_{p}"

# Machine time constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"MachineAvailability_Constraint_{m}"

# Solve the problem
problem.solve()

# Output results
batches_produced = [int(batches[p].varValue) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_produced,
    "total_profit": total_profit
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')