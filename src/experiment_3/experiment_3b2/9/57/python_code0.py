import pulp

# Data from JSON
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Initialize the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("unloaded", range(1, data['T'] + 1), lowBound=0, upBound=None)  # Number of containers unloaded
y = pulp.LpVariable.dicts("cranes", range(1, data['T'] + 1), lowBound=0, cat='Integer')  # Number of cranes rented
s = pulp.LpVariable.dicts("inventory", range(1, data['T'] + 1), lowBound=0)  # Inventory at the end of each month

# Objective Function
problem += pulp.lpSum(data['UnloadCosts'][t-1] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(1, data['T'] + 1))

# Constraints
for t in range(1, data['T'] + 1):
    problem += x[t] <= data['UnloadCapacity'][t-1], f"Unload_Capacity_Constraint_{t}"

problem += s[1] == data['InitContainer'] + x[1] - data['Demands'][0], "Initial_Inventory_Constraint"

for t in range(2, data['T'] + 1):
    problem += s[t] == s[t-1] + x[t] - data['Demands'][t-1], f"Inventory_Balance_Constraint_{t}"

for t in range(1, data['T'] + 1):
    problem += s[t] <= data['MaxContainer'], f"Max_Container_Constraint_{t}"
    problem += y[t] * data['CraneCapacity'] >= data['Demands'][t-1], f"Cranes_Capacity_Constraint_{t}"
    problem += y[t] <= data['NumCranes'], f"Max_Cranes_Constraint_{t}"

problem += s[data['T']] == 0, "Final_Inventory_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')