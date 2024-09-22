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

# Problem variables
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

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Integer')

# Objective function
profit = pulp.lpSum((prices[p] - pulp.lpSum(machine_costs[m] * (time_required[m][p] / 100)) - 
                pulp.lpSum((pulp.lpMax(0, (time_required[m][p] * batches[p] - availability[m])) * 
                overtime_cost + (standard_cost * pulp.lpMin(time_required[m][p] * batches[p], availability[m]))))
                for m in range(M))) * batches[p] for p in range(P))

problem += profit, "Total Profit"

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_{p}"

# Machine time constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"MachineAvailability_{m}"

# Solve the problem
problem.solve()

# Get the results
batches_result = [int(batches[p].varValue) for p in range(P)]
total_profit = pulp.value(problem.objective)

# Output format
result = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')