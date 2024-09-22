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

# Decision Variables
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create the LP problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Define decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function: Maximize profit
problem += pulp.lpSum(
    (prices[p] - pulp.lpSum(machine_costs[m] * time_required[m][p] for m in range(M))) * batches[p] for p in range(P)
), "Total Profit")

# Constraints
# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Availability_Machine_{m}"

# Minimum batches constraint
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_Part_{p}"

# Overtime and standard costs
# This part only applies to machine 1 and is a simplified approach
problem += pulp.lpSum(time_required[0][p] * batches[p] for p in range(P)) <= overtime_hour[0], "Standard_Hours_Machine_1"
problem += pulp.lpSum((time_required[0][p] * batches[p] - overtime_hour[0]) for p in range(P)) <= 0, "Overtime_Hours_Machine_1")

# Solve the problem
problem.solve()

# Output results
batches_result = [int(batches[p].value()) for p in range(P)]
total_profit = pulp.value(problem.objective)

output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')