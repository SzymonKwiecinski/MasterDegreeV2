import pulp

# Data from the JSON
data = {'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
        'StorageCost': 5, 'SwitchCost': 10}

# Initialize the problem
problem = pulp.LpProblem("Production_and_Inventory_Schedule", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpContinuous)
I = pulp.LpVariable.dicts("I", range(1, data['T'] + 1), lowBound=0, cat=pulp.LpContinuous)

# Objective Function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
           pulp.lpSum(data['SwitchCost'] * pulp.lpSum([pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, data['T'])]))

# Constraints
# Initial Inventory
problem += I[1] == x[1] - data['Deliver'][0]

# Inventory balance constraints
for i in range(2, data['T'] + 1):
    problem += I[i] == I[i - 1] + x[i] - data['Deliver'][i - 1]

# Final inventory should be zero
problem += I[data['T']] == 0

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')