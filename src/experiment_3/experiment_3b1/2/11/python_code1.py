import pulp

# Data from the provided JSON
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Create the problem variable
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Production", range(data['T']), lowBound=0)  # Production in each month
I = pulp.LpVariable.dicts("Inventory", range(data['T'] + 1), lowBound=0)  # Inventory at the end of each month

# Objective Function
problem += pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
            pulp.lpSum(data['SwitchCost'] * (x[i] - x[i - 1]) for i in range(1, data['T'])), "Total_Cost"

# Constraints
problem += I[0] == 0  # Initial inventory

# Inventory balance constraints
for i in range(data['T']):
    problem += I[i + 1] == I[i] + x[i] - data['Deliver'][i], f"Inventory_Balance_{i + 1}"

# Final inventory constraint
problem += I[data['T']] == 0, "Final_Inventory_Zero"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')