import pulp
import json

# Load data from json format
data = json.loads("{'NumMachines': 3, 'NumParts': 4, 'TimeRequired': [[2, 1, 3, 2], [4, 2, 1, 2], [6, 2, 1, 2]], 'MachineCosts': [160, 10, 15], 'Availability': [200, 300, 500], 'Prices': [570, 250, 585, 430], 'MinBatches': [10, 10, 10, 10], 'StandardCost': 20, 'OvertimeCost': 30, 'OvertimeHour': [400, 400, 300]}")

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
num_parts = data['NumParts']
x = pulp.LpVariable.dicts("Batch", range(num_parts), lowBound=0)

# Objective function
profit_terms = [data['Prices'][p] * x[p] for p in range(num_parts)]
cost_terms = [
    sum(data['MachineCosts'][m] * data['TimeRequired'][m][p] * x[p] for p in range(num_parts)) for m in range(data['NumMachines'])
]
problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms)

# Constraints
# Minimum production requirement
for p in range(num_parts):
    problem += x[p] >= data['MinBatches'][p]

# Machine availability constraints
for m in range(1, data['NumMachines']):
    problem += pulp.lpSum(data['TimeRequired'][m][p] * x[p] for p in range(num_parts)) <= data['Availability'][m]

# Outsourced machine 1 costs
machine_1_time = pulp.lpSum(data['TimeRequired'][0][p] * x[p] for p in range(num_parts))
problem += machine_1_time <= data['OvertimeHour'][0] + (data['Availability'][0] / 8)

# Non-negativity constraints are inherently handled by lower bound in variables

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')