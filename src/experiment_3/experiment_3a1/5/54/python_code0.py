import pulp
import json

# Load data from JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour_limits = data['OvertimeHour']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable("Overtime_Hours", lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(prices[p] * batches[p] for p in range(P)) \
         - pulp.lpSum(costs[m] * time_required[m][p] * batches[p] for p in range(P) for m in range(M)) \
         - (standard_cost * overtime_hours + overtime_cost * pulp.max(0, overtime_hours - pulp.lpSum(overtime_hour_limits)))
problem += profit, "Total_Profit"

# Constraints
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m], f"Machine_Availability_{m}"

# Solve the problem
problem.solve()

# Output results
for p in range(P):
    print(f'Batches produced for part {p}: {batches[p].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')