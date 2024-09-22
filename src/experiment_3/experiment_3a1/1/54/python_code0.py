import pulp
import json

# Load the data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = pulp.LpVariable.dicts("batches", range(P), lowBound=0)

# Objective function
profit = pulp.lpSum([prices[p] * batches[p] for p in range(P)])  # Total revenue
machine_cost = pulp.lpSum([machine_costs[m] * pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) for m in range(M)])  # Total machine cost
labor_cost = pulp.lpSum([pulp.lpSum([standard_cost * min(availability[m] / sum(time_required[m][p] * batches[p] for p in range(P)), overtime_hour[m]) + \
                                       overtime_cost * (availability[m] / sum(time_required[m][p] * batches[p] for p in range(P)) - overtime_hour[m])
                                       for m in range(M)])])

problem += profit - machine_cost - labor_cost, "Total_Profit"

# Constraints
# Machine time constraints
for m in range(M):
    problem += pulp.lpSum([time_required[m][p] * batches[p] for p in range(P)]) <= availability[m], f"Machine_Availability_{m}"

# Minimum production requirement
for p in range(P):
    problem += batches[p] >= min_batches[p], f"Min_Batches_{p}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')