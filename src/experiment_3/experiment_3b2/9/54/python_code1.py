import pulp
import json

# Input data
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Extract data
NumMachines = data['NumMachines']
NumParts = data['NumParts']
TimeRequired = data['TimeRequired']
MachineCosts = data['MachineCosts']
Availability = data['Availability']
Prices = data['Prices']
MinBatches = data['MinBatches']
StandardCost = data['StandardCost']
OvertimeCost = data['OvertimeCost']
OvertimeHour = data['OvertimeHour']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(NumParts), lowBound=0, cat='Continuous')

# Additional labor cost
total_labor_cost_m = 0  # Initialize total labor cost
for m in range(1, NumMachines):
    total_time_m = pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(NumParts)])
    if m == 1:
        total_labor_cost_m = (pulp.lpSum([StandardCost * total_time_m if total_time_m <= OvertimeHour[m] 
                                            else StandardCost * OvertimeHour[m] + OvertimeCost * (total_time_m - OvertimeHour[m])]))

# Objective function
profit = pulp.lpSum([Prices[p] * x[p] for p in range(NumParts)]) - \
         (pulp.lpSum([MachineCosts[m] * (pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(NumParts)])) for m in range(NumMachines)]) + total_labor_cost_m)
problem += profit

# Constraints for machine time
for m in range(1, NumMachines):
    problem += pulp.lpSum([TimeRequired[m][p] * x[p] for p in range(NumParts)]) <= Availability[m]

# Contractual obligations
for p in range(NumParts):
    problem += x[p] >= MinBatches[p]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')