import pulp
import json

# Input data
data_json = '''{
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
data = json.loads(data_json)

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
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)]) - \
         pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])

problem += profit

# Constraints
# Production constraints for each part
for p in range(P):
    problem += batches[p] >= min_batches[p], f"MinBatches_constraint_part_{p}"

# Machine availability constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Availability_constraint_machine_{m}"

# Labor cost constraints for Machine 1
T = pulp.lpSum([time_required[0][p] * batches[p] for p in range(P)])
problem += (T <= overtime_hour[0]) | (standard_cost * T + overtime_cost * (T - overtime_hour[0]) >= 0), "Machine_1_Cost_Constraint"

# Solve the problem
problem.solve()

# Output results
batches_solution = {p: batches[p].varValue for p in range(P)}
total_profit = pulp.value(problem.objective)

print("Batches Produced:", batches_solution)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')