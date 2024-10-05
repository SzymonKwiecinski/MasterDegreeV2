import pulp

# Input data
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

# Parameters
P = data['NumParts']
M = data['NumMachines']
time_required = data['TimeRequired']
costs = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Define the problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables: batches of each part
batches = pulp.LpVariable.dicts("Batches", range(P), lowBound=0, cat='Continuous')

# Objective function components
revenue = pulp.lpSum(prices[p] * batches[p] for p in range(P))
production_cost = pulp.lpSum(costs[m] * pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) for m in range(M))

# Labor cost calculation for machine 1
T1 = pulp.lpSum(time_required[0][p] * batches[p] for p in range(P))
labor_cost = pulp.LpVariable("LaborCost", lowBound=0, cat='Continuous')

# Labor cost constraints for machine 1
problem += labor_cost >= standard_cost * T1
problem += labor_cost >= standard_cost * overtime_hour[0] + overtime_cost * (T1 - overtime_hour[0])

# Objective function
problem += revenue - production_cost - labor_cost

# Constraints
# 1. Machine time constraints
for m in range(M):
    problem += pulp.lpSum(time_required[m][p] * batches[p] for p in range(P)) <= availability[m]

# 2. Minimum batches requirement
for p in range(P):
    problem += batches[p] >= min_batches[p]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')