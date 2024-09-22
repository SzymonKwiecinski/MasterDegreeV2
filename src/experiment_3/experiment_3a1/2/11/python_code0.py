import pulp
import json

# Load data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')

# Parameters
T = data['T']
deliver = data['Deliver']
c_s = data['StorageCost']
c_w = data['SwitchCost']

# Create the problem
problem = pulp.LpProblem("Production_Inventory_Scheduling", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Integer')
I = pulp.LpVariable.dicts("Inventory", range(0, T + 1), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(c_s * I[i] for i in range(1, T + 1)) + pulp.lpSum(c_w * pulp.lpSum(abs(x[i] - x[i - 1]) for i in range(2, T + 1)))

# Constraints
problem += I[0] == 0  # Initial inventory

for i in range(1, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  # Inventory balance
    problem += I[i] >= 0  # Non-negative inventory

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')