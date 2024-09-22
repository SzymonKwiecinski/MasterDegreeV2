import json
import pulp

# Load data from the provided JSON format
data = json.loads('{"NumMachines": 3, "NumParts": 4, "TimeRequired": [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], "MachineCosts": [160, 10, 15], "Availability": [200, 300, 500], "Prices": [570, 250, 585, 430], "MinBatches": [10, 10, 10, 10], "StandardCost": 20, "OvertimeCost": 30, "OvertimeHour": [400, 400, 300]}')

# Number of machines and parts
num_machines = data['NumMachines']
num_parts = data['NumParts']

# Create the Linear Programming problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables: batches produced for each part
batches = pulp.LpVariable.dicts("batches", range(num_parts), lowBound=0)

# Objective function
labor_cost = pulp.lpSum(
    (data['StandardCost'] * pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(num_parts))
     + pulp.lpSum(data['OvertimeCost'] * (pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(num_parts)) 
     - data['OvertimeHour'][0]) for m in range(num_machines) if pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) > data['OvertimeHour'][m])
    )
)
total_profit = pulp.lpSum(data['Prices'][p] * batches[p] for p in range(num_parts)) - pulp.lpSum(
    data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts))
    for m in range(num_machines)
) - labor_cost

problem += total_profit

# Constraints for machine availability
for m in range(num_machines):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(num_parts)) <= data['Availability'][m]

# Constraints for minimum production
for p in range(num_parts):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Output the results
for p in range(num_parts):
    print(f'Batches of part {p + 1}: {pulp.value(batches[p])}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')