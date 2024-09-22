import pulp

# Input data
data = {
    'T': 12,
    'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    'StorageCost': 5,
    'SwitchCost': 10
}

# Define the LP problem
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, data['T'] + 1), lowBound=0, cat='Continuous')
I = pulp.LpVariable.dicts("I", range(1, data['T'] + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    data['StorageCost'] * I[i] + data['SwitchCost'] * pulp.lpSum([pulp.LpVariable(f"abs_diff_{i+1}_{i}", lowBound=0) for i in range(1, data['T'])])
    for i in range(1, data['T'] + 1)
)

# Constraints
# Inventory continuity constraints
problem += (I[0] == 0, "Initial Inventory Constraint")

for i in range(1, data['T'] + 1):
    if i == 1:
        problem += (I[i] == x[i] - data['Deliver'][i-1], f"Inventory_Constraint_{i}")
    else:
        problem += (I[i] == I[i-1] + x[i] - data['Deliver'][i-1], f"Inventory_Constraint_{i}")

# Absolute difference constraints for switch cost
for i in range(1, data['T']):
    abs_diff = pulp.LpVariable(f"abs_diff_{i+1}_{i}", lowBound=0, cat='Continuous')
    problem += (abs_diff >= x[i+1] - x[i], f"Abs_Positive_Diff_Constraint_{i}")
    problem += (abs_diff >= x[i] - x[i+1], f"Abs_Negative_Diff_Constraint_{i}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')