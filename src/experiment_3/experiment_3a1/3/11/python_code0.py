import pulp

# Data from the provided JSON format
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0)  # Production each month
I = pulp.LpVariable.dicts("Inventory", range(1, data['T'] + 1), lowBound=0)   # Inventory each month

# Objective Function
problem += pulp.lpSum(data['StorageCost'] * I[i] + 
                       data['SwitchCost'] * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, data['T'])) + \
                       data['StorageCost'] * I[data['T']]), "Total_Cost"

# Constraints
# Inventory for the first month
problem += I[1] == x[1] - data['Deliver'][0], "Inventory_1"

# Inventory for the months 2 to T
for i in range(2, data['T'] + 1):
    problem += I[i] == I[i - 1] + x[i] - data['Deliver'][i - 1], f"Inventory_{i}"

# Ensuring non-negativity of the inventory at the last month
problem += I[data['T']] >= 0, "Nonnegativity_Invent_T"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')