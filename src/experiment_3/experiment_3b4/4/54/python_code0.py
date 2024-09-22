import pulp

# Data
data = {
    'NumMachines': 3,
    'NumParts': 4,
    'TimeRequired': [
        [2, 1, 3, 2],  # Machine 1
        [4, 2, 1, 2],  # Machine 2
        [6, 2, 1, 2]   # Machine 3
    ],
    'MachineCosts': [160, 10, 15],
    'Availability': [200, 300, 500],
    'Prices': [570, 250, 585, 430],
    'MinBatches': [10, 10, 10, 10],
    'StandardCost': 20,
    'OvertimeCost': 30,
    'OvertimeHour': [400, 400, 300]
}

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f"x_{p+1}", lowBound=data['MinBatches'][p], cat='Continuous') for p in range(data['NumParts'])]

# Objective Function
profit_terms = [data['Prices'][p] * x[p] for p in range(data['NumParts'])]

machine_costs_terms = []
for m in range(1, data['NumMachines']):
    for p in range(data['NumParts']):
        machine_costs_terms.append(data['MachineCosts'][m] * data['TimeRequired'][m][p] * x[p])

machine_1_labor_time = pulp.lpSum([data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts'])])

labor_cost_machine_1 = (data['StandardCost'] * min(machine_1_labor_time, data['OvertimeHour'][0]) +
                        data['OvertimeCost'] * max(machine_1_labor_time - data['OvertimeHour'][0], 0))

problem += pulp.lpSum(profit_terms) - pulp.lpSum(machine_costs_terms) - labor_cost_machine_1

# Constraints
# Demand Constraints
for p in range(data['NumParts']):
    problem += x[p] >= data['MinBatches'][p]

# Machine Availability Constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum([data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])]) <= data['Availability'][m]

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')