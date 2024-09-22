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

# Create the LP problem
problem = pulp.LpProblem("Auto_Parts_Manufacturing", pulp.LpMaximize)

# Decision variables
x = {p: pulp.LpVariable(f"x_{p}", lowBound=data['MinBatches'][p]) for p in range(data['NumParts'])}

# Objective function components
profit_terms = [data['Prices'][p] * x[p] for p in range(data['NumParts'])]
machine1_usage = sum(data['TimeRequired'][0][p] * x[p] for p in range(data['NumParts']))

# Calculate Labor cost for Machine 1
if machine1_usage <= data['OvertimeHour'][0]:
    labor_cost = data['StandardCost'] * machine1_usage
else:
    labor_cost = data['StandardCost'] * data['OvertimeHour'][0] + data['OvertimeCost'] * (machine1_usage - data['OvertimeHour'][0])

# Objective Function
profit = sum(profit_terms) - labor_cost - sum(
    data['MachineCosts'][m] * sum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts']))
    for m in range(1, data['NumMachines'])
)

problem += profit

# Constraints
# Machine time availability constraints for each machine (except machine 1 due to dynamic labor cost)
for m in range(1, data['NumMachines']):
    problem += sum(data['TimeRequired'][m][p] * x[p] for p in range(data['NumParts'])) <= data['Availability'][m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')