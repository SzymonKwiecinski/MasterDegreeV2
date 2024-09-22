import pulp
import json

# Load the data
data_json = """{
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
}"""

data = json.loads(data_json)

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Batches", range(data['NumParts']), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts'])) \
    - pulp.lpSum(data['MachineCosts'][m-1] * pulp.lpSum(data['TimeRequired'][m-1][p] * x[p] for p in range(data['NumParts'])) for m in range(2, data['NumMachines'] + 1)) \
    - (pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) * 
       pulp.lpSum([data['StandardCost'], data['OvertimeCost']][int(pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])) > data['OvertimeHour'][0])])))

# Constraints
# Production requirements
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"MinBatches_Constraint_{p}"

# Machine availability (except for machine 1)
for m in range(2, data['NumMachines'] + 1):
    problem += pulp.lpSum(data['TimeRequired'][m-1][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m-1], f"MachineAvailability_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')