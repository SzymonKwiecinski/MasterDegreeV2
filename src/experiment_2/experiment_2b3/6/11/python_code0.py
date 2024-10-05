import pulp

# Data
data = {
    "T": 12,
    "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100],
    "StorageCost": 5,
    "SwitchCost": 10
}

# Problem
problem = pulp.LpProblem("Production_Plan", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x{i}", lowBound=0, cat='Continuous') for i in range(data["T"])]
inventory = [pulp.LpVariable(f"inventory{i}", lowBound=0, cat='Continuous') for i in range(data["T"])]

# Objective function
total_cost = (
    pulp.lpSum(data["StorageCost"] * inventory[i] for i in range(data["T"])) +
    pulp.lpSum(data["SwitchCost"] * abs(x[i + 1] - x[i]) for i in range(data["T"] - 1))
)
problem += total_cost

# Initial inventory constraint
problem += inventory[0] == x[0] - data["Deliver"][0]

# Inventory balance constraints
for i in range(1, data["T"]):
    problem += inventory[i] == inventory[i - 1] + x[i] - data["Deliver"][i]

# Solve
problem.solve()

# Results
x_values = [pulp.value(x[i]) for i in range(data["T"])]
total_cost_value = pulp.value(problem.objective)

output = {
    "x": x_values,
    "cost": total_cost_value
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')