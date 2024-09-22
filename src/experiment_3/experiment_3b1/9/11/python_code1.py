import pulp
import json

# Input data
data = json.loads("{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}")
T = data['T']
deliver = data['Deliver']
c_s = data['StorageCost']
c_w = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts('x', range(1, T + 1), lowBound=0)  # Production amounts
I = pulp.LpVariable.dicts('I', range(1, T + 1), lowBound=0)  # Inventory amounts

# Objective function
problem += pulp.lpSum(c_s * I[i] + c_w * (x[i + 1] - x[i]) for i in range(1, T)) + c_s * I[T] for i in range(1, T + 1))

# Constraints
I[1] = x[1] - deliver[0]  # Inventory balance for month 1
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1], f"Inventory_Balance_{i}"

# Last month inventory condition
problem += I[T] == 0, "Last_Month_Inventory"

# Solve the problem
problem.solve()

# Output the production schedule and objective value
x_values = [x[i].varValue for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Production schedule: {x_values}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')