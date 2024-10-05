import pulp

# Data from the provided JSON
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("batches", range(data['NumParts']), lowBound=0)

# Calculate T1
T1 = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))

# Labor cost for Machine 1
labor_cost_m1 = pulp.LpVariable("labor_cost_m1")

# Labor cost expression
labor_cost_expr = pulp.lpSum([
    data['StandardCost'] * T1 if T1 <= data['OvertimeHour'][0] else 
    data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'][0] * (T1 - data['OvertimeHour'][0])
])

# Objective function
profit = pulp.lpSum(data['Prices'][p] * x[p] for p in range(data['NumParts'])) - \
         pulp.lpSum(data['MachineCosts'][m] * pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) for m in range(1, data['NumMachines'])) - \
         labor_cost_expr

problem += profit

# Constraints

# Minimum production requirement for each part
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p], f"MinBatch_Constraint_{p}"

# Machine availability constraints (except Machine 1)
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m], f"MachineAvailability_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')