import pulp
import json

# Input data
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

# Decision variables
x = pulp.LpVariable.dicts("batches", range(P), lowBound=0, cat='Continuous')

# Problem definition
problem = pulp.LpProblem("Production_Planning", pulp.LpMaximize)

# Objective Function
C1 = pulp.LpVariable("C1", lowBound=0)
overtime_hours = [pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) - overtime_hour[m-2] for m in range(2, M+1)]
problem += pulp.lpSum(prices[p] * x[p] for p in range(P)) - pulp.lpSum(machine_costs[m-1] * pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) for m in range(2, M+1)) - \
    (pulp.lpSum(standard_cost * pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) if pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) <= overtime_hour[0] else \
    (standard_cost * overtime_hour[0] + overtime_cost * overtime_hours[0]) for m in range(2, M+1)))

# Constraints
for p in range(P):
    problem += x[p] >= min_batches[p], f"MinBatches_Constraint_{p+1}"
    
for m in range(2, M + 1):
    problem += pulp.lpSum(time_required[m-1][p] * x[p] for p in range(P)) <= availability[m-1], f"Machine_Availability_Constraint_{m-1}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')