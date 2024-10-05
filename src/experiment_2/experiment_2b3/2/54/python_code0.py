import pulp

# Unpack the JSON data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
batches = [pulp.LpVariable(f'Batch_{p}', lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]
machine_1_hours = pulp.LpVariable('Machine_1_Hours', lowBound=0, cat='Continuous')
overtime_hours = pulp.LpVariable('Overtime_Hours', lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
profit = pulp.lpSum([batches[p] * data['Prices'][p] for p in range(data['NumParts'])])
machine_costs = pulp.lpSum([pulp.lpSum([data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])]) * data['MachineCosts'][m] for m in range(1, data['NumMachines'])])
labor_costs = machine_1_hours * data['StandardCost'] + overtime_hours * data['OvertimeCost']

problem += profit - machine_costs - labor_costs, "Total_Profit"

# Constraints

# Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum([data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])]) <= data['Availability'][m], f"Availability_M{m}"

# Machine 1 special condition
problem += machine_1_hours == pulp.lpSum([data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts'])]), "Machine_1_Hours_Calc"
problem += machine_1_hours == overtime_hours + data['OvertimeHour'][0], "Machine_1_Overtime_Hours_Constraint"

# Solve the problem
problem.solve()

# Collect results
batches_result = [pulp.value(batches[p]) for p in range(data['NumParts'])]
total_profit = pulp.value(problem.objective)

# Output format
output = {
    "batches": batches_result,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')