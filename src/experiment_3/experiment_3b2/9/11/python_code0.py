import pulp

# Data from JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

T = data['T']
d = data['Deliver']
c_s = data['StorageCost']
c_switch = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0)  # Production per month
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0)  # Inventory at the end of month
z = pulp.LpVariable.dicts("Switch", range(1, T), lowBound=0)  # Change in production level

# Objective Function
problem += pulp.lpSum(c_s * I[i] for i in range(1, T + 1)) + pulp.lpSum(c_switch * z[i] for i in range(1, T)), "Total_Cost"

# Constraints

# Inventory Balance
problem += (I[1] == x[1] + 0 - d[0]), "Inventory_Balance_1"  # I_0 = 0
for i in range(2, T + 1):
    problem += (I[i] == x[i] + I[i - 1] - d[i - 1]), f"Inventory_Balance_{i}"

# Production Switch Adjustment
for i in range(1, T):
    problem += (z[i] >= x[i + 1] - x[i]), f"Switch_Upper_{i}"
    problem += (z[i] >= x[i] - x[i + 1]), f"Switch_Lower_{i}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(1, T + 1):
    print(f'Production in month {i}: {x[i].varValue}, Inventory at end of month {i}: {I[i].varValue}')