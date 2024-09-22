import pulp

# Load data from JSON format
data = {
    'T': 12, 
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 
    'StorageCost': 5, 
    'SwitchCost': 10
}

# Define the problem
problem = pulp.LpProblem("Production_Inventory_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0)   # units produced
inv = pulp.LpVariable.dicts("Inventory", range(1, data['T'] + 1), lowBound=0)    # inventory at the end of month

# Objective Function
problem += pulp.lpSum(data['StorageCost'] * inv[i] for i in range(1, data['T'] + 1)) \
           + pulp.lpSum(data['SwitchCost'] * (x[i + 1] - x[i]) for i in range(1, data['T'])) \
           + pulp.lpSum(data['SwitchCost'] * (x[i] - x[i + 1]) for i in range(1, data['T']))  # Adding the absolute difference

# Constraints
# Inventory balance equation with initial condition inv_0 = 0
problem += inv[1] == x[1] - data['Deliver'][0]

for i in range(2, data['T'] + 1):
    problem += inv[i] == inv[i - 1] + x[i] - data['Deliver'][i - 1]

# Last month's inventory has no storage cost
problem += inv[data['T']] == 0

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')