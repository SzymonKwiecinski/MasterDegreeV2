import pulp
import json

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

# Extract data from input
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

# Define decision variables
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Continuous')

# Objective function: Maximize profit
profit = pulp.lpSum((prices[p] * batches[p] - 
                     pulp.lpSum((time_required[m][p] * batches[p] / 100) * machine_costs[m] for m in range(num_machines))
                     ) for p in range(num_parts))
                    )
problem += profit

# Constraints for machine availability
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m]

# Constraints for minimum batches
for p in range(num_parts):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Prepare the output
output_batches = [pulp.value(batches[p]) for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Print results
output = {
    "batches": output_batches,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')