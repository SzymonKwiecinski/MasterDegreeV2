import pulp

# Data from json
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

# Unpack the data
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
machine_costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{p}', lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
profit_terms = [prices[p] * x[p] for p in range(P)]
cost_terms = [
    machine_costs[m] * pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) 
    for m in range(M)
]

labor_cost_part = (
    standard_cost * pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) +
    overtime_cost * pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) - overtime_hour[0]
)

# Adjust labor cost part for actual overtime calculations
labor_cost_corrected = (
    standard_cost * min(overtime_hour[0], pulp.lpSum(time_required[0][p] * x[p] for p in range(P))) +
    overtime_cost * max(0, pulp.lpSum(time_required[0][p] * x[p] for p in range(P)) - overtime_hour[0])
)

problem += pulp.lpSum(profit_terms) - pulp.lpSum(cost_terms) - labor_cost_corrected

# Constraints
# Minimum Production Requirement
for p in range(P):
    problem += x[p] >= min_batches[p]

# Machine Availability
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * x[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')