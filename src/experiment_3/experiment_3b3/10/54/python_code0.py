import pulp

# Data
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

# Indices
P = data['NumParts']
M = data['NumMachines']

# Decision Variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Objective Function
profit_terms = [data['Prices'][p] * batches[p] - 
                data['MachineCosts'][m] * data['TimeRequired'][m][p] * batches[p]
                for m in range(M) for p in range(P)]
labor_cost_machine_1_terms = [
    pulp.lpSum(
        data['StandardCost'] * data['TimeRequired'][0][p] * batches[p]
        if data['TimeRequired'][0][p] * batches[p] <= data['OvertimeHour'][0]
        else data['StandardCost'] * data['OvertimeHour'][0] + 
             data['OvertimeCost'] * (data['TimeRequired'][0][p] * batches[p] - data['OvertimeHour'][0])
    )
    for p in range(P)
]

problem += pulp.lpSum(profit_terms) - pulp.lpSum(labor_cost_machine_1_terms)

# Constraints
# Machine Availability Constraints
for m in range(M):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * batches[p] for p in range(P)) <= data['Availability'][m]

# Minimum Production Requirements
for p in range(P):
    problem += batches[p] >= data['MinBatches'][p]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')