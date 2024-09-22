import pulp

# Data from the problem
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("Production", range(1, data['T'] + 1), lowBound=0)
I = pulp.LpVariable.dicts("Inventory", range(1, data['T'] + 1), lowBound=0)

# Objective Function
objective = pulp.lpSum(data['StorageCost'] * I[i] for i in range(1, data['T'] + 1)) + \
            pulp.lpSum(data['SwitchCost'] * (x[i+1] - x[i]) for i in range(1, data['T'])) + \
            pulp.lpSum(data['SwitchCost'] * (x[i] - x[i+1]) for i in range(1, data['T'])) 

problem += objective

# Constraints
# Inventory balance for each month
I[1] = x[1] - data['Deliver'][0]  # I_1 = x_1 - deliver_1
for i in range(2, data['T'] + 1):
    problem += I[i] == I[i-1] + x[i] - data['Deliver'][i-1], f"Inventory_Balance_{i}"

# Ensure inventory must be non-negative
for i in range(1, data['T'] + 1):
    problem += I[i] >= 0, f"Non_Negative_Inventory_{i}"

# Production decision for the last month
problem += I[data['T']] == 0, "Inventory_Zero_Last_Month"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')