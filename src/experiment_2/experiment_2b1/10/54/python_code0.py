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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Extracting data
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

# Decision variables
batches = pulp.LpVariable.dicts("Batches", range(num_parts), lowBound=0, cat='Integer')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(num_parts)) - \
         pulp.lpSum((pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) * machine_costs[m] / 100) \
         for m in range(num_machines))

problem += profit, "Total_Profit"

# Constraints
# Machine availability constraints
for m in range(num_machines):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(num_parts)) <= availability[m], f"Availability_Constraint_Machine_{m + 1}"

# Minimum batches constraints
for p in range(num_parts):
    problem += batches[p] >= min_batches[p], f"Min_Batch_Constraint_Part_{p + 1}"

# Solve the problem
problem.solve()

# Prepare output
output_batches = [batches[p].varValue for p in range(num_parts)]
total_profit = pulp.value(problem.objective)

# Output results
output = {
    "batches": output_batches,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')