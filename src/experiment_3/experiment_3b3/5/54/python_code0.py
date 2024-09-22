import pulp

# Data input
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

# Initialize problem
problem = pulp.LpProblem("AutoPartsManufacturer", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'b_{p}', lowBound=data['MinBatches'][p], cat='Continuous') 
           for p in range(data['NumParts'])]

# Objective function
profit_terms = [data['Prices'][p] * batches[p] for p in range(data['NumParts'])]
cost_terms = [
    sum(data['MachineCosts'][m] * data['TimeRequired'][m][p] / 100 * batches[p] 
        for m in range(data['NumMachines']))
    for p in range(data['NumParts'])
]
standard_labor_cost = pulp.lpSum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))
overtime_cost = data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (standard_labor_cost - data['OvertimeHour'][0])
overtime_condition = standard_labor_cost > data['OvertimeHour'][0]

total_cost = pulp.lpSum(cost_terms)

labor_cost = pulp.LpVariable("labor_cost", cat='Continuous')
problem += labor_cost >= data['StandardCost'] * standard_labor_cost
problem += labor_cost >= (overtime_cost if overtime_condition else data['StandardCost'] * standard_labor_cost)

problem += pulp.lpSum(profit_terms) - total_cost - labor_cost

# Constraints
# Machine availability constraints
for m in range(data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solving the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')