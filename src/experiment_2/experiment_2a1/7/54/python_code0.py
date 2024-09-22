import pulp
import json

data = {'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}

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
overtime_hours = data['OvertimeHour']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: number of batches for each part
batches = [pulp.LpVariable(f'batches_{p}', lowBound=min_batches[p], cat='Integer') for p in range(num_parts)]

# Objective function: maximize profit
profit = pulp.lpSum(
    (prices[p] * batches[p]) - pulp.lpSum(
        [(time_required[m][p] * machine_costs[m] * batches[p]) for m in range(num_machines)]
    ) for p in range(num_parts))
)
problem += profit, "Total_Profit"

# Constraints for machine availability
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"Availability_Machine_{m}"

# Solve the problem
problem.solve()

# Extract results
batches_solution = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output preparation
output = {
    "batches": batches_solution,
    "total_profit": total_profit
}

print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')