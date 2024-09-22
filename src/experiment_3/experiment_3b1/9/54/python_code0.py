import pulp
import json

# Data provided in JSON format
data = '''{
    "NumMachines": 3,
    "NumParts": 4,
    "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]],
    "MachineCosts": [160, 10, 15],
    "Availability": [200, 300, 500],
    "Prices": [570, 250, 585, 430],
    "MinBatches": [10, 10, 10, 10],
    "StandardCost": 20,
    "OvertimeCost": 30,
    "OvertimeHour": [400, 400, 300]
}'''

# Load the data
data = json.loads(data)

# Parameters
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

# Decision Variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
hours_used_1 = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])

labor_cost = pulp.lpSum([
    standard_cost * hours_used_1 if hours_used_1 <= overtime_hour[m]
    else standard_cost * overtime_hour[m] + overtime_cost * (hours_used_1 - overtime_hour[m])
    for m in range(M)
])

total_profit = (pulp.lpSum([prices[p] * batches[p] for p in range(P)]) 
                 - pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)]) 
                 - labor_cost)

problem += total_profit, "Total_Profit"

# Constraints
# Machine capacity constraints
for m in range(M):
    problem += (pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], 
                           f"Machine_Capacity_Constraint_{m}")

# Minimum production constraints
for p in range(P):
    problem += (batches[p] >= min_batches[p], f"Min_Batches_Constraint_{p}")

# Solve the problem
problem.solve()

# Output
for p in range(P):
    print(f'Batches of part {p + 1}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')