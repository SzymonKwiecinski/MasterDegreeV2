import pulp

# Load the data
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

# Initialize the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
batches = [pulp.LpVariable(f'batches_{p}', lowBound=data['MinBatches'][p], cat='Integer')
           for p in range(data['NumParts'])]

# Overtime hours on machine m=1
overtime_hours = pulp.LpVariable('overtime_hours', lowBound=0, cat='Continuous')

# Objective function: Maximize total profit
profit_terms = [
    batches[p] * data['Prices'][p] for p in range(data['NumParts'])
]

# Cost for machines
cost_machine = [
    sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) * data['MachineCosts'][m]
    for m in range(1, data['NumMachines'])
]

# Machine 1 cost calculation with separate overtime consideration
time_on_machine_1 = sum(data['TimeRequired'][0][p] * batches[p] for p in range(data['NumParts']))
cost_machine_1 = (
    min(time_on_machine_1, data['OvertimeHour'][0]) * data['StandardCost'] +
    overtime_hours * data['OvertimeCost']
)

# Calculate profit
total_profit = sum(profit_terms) - sum(cost_machine) - cost_machine_1

# Set objective
problem += total_profit

# Constraints for each machine except machine 1
for m in range(1, data['NumMachines']):
    problem += (
        sum(data['TimeRequired'][m][p] * batches[p] for p in range(data['NumParts'])) <= data['Availability'][m]
    )

# Overtime calculation for machine 1
problem += time_on_machine_1 <= data['OvertimeHour'][0] + overtime_hours

# Solve the problem
problem.solve()

# Retrieve the result
solution = {
    "batches": [int(batches[p].varValue) for p in range(data['NumParts'])],
    "total_profit": pulp.value(problem.objective)
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')