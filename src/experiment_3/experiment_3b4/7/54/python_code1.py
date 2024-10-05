import pulp

# Data provided
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

# Unpacking data
P = data['NumParts']
M = data['NumMachines']
time = data['TimeRequired']
cost = data['MachineCosts']
availability = data['Availability']
prices = data['Prices']
min_batches = data['MinBatches']
standard_cost = data['StandardCost']
overtime_cost = data['OvertimeCost']
overtime_hour = data['OvertimeHour']

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f"x_{p}", lowBound=0, cat='Continuous') for p in range(P)]

# Objective Function
overtime_usage = pulp.lpSum(time[0][p] * x[p] for p in range(P))

profit = (pulp.lpSum(prices[p] * x[p] for p in range(P))
          - pulp.lpSum(cost[m] * pulp.lpSum(time[m][p] * x[p] for p in range(P)) for m in range(1, M))
          - (standard_cost * pulp.lpSum(time[0][p] * x[p] for p in range(P)))
          - overtime_cost * pulp.lpSum([pulp.lpMax(0, overtime_usage - overtime_hour[0])]))

problem += profit

# Constraints
# Minimum production constraints
for p in range(P):
    problem += x[p] >= min_batches[p]

# Machine availability constraints (excluding machine 1)
for m in range(1, M):
    problem += pulp.lpSum(time[m][p] * x[p] for p in range(P)) <= availability[m]

# Solve the problem
problem.solve()

# Print the output
print(f"(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")