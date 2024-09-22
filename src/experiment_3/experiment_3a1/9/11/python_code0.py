import pulp
import json

# Load data
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the Linear Programming problem
problem = pulp.LpProblem("Production_Problem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts("x", range(1, T + 1), lowBound=0, cat='Continuous')  # Production variables
I = pulp.LpVariable.dicts("I", range(1, T + 1), lowBound=0, cat='Continuous')  # Inventory variables

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T))

# Constraints
problem += I[1] == x[1] - deliver[0]  # Inventory balance for month 1
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliver[i - 1]  # Inventory balance for months 2 to T

# Non-negativity of inventory
for i in range(1, T + 1):
    problem += I[i] >= 0

# Non-negativity of production
for i in range(1, T + 1):
    problem += x[i] >= 0

# End of the year inventory
problem += I[T] == 0

# Solve the problem
problem.solve()

# Output
production_schedule = [x[i].varValue for i in range(1, T + 1)]
minimized_cost = pulp.value(problem.objective)

print(f'Production Schedule: {production_schedule}')
print(f' (Objective Value): <OBJ>{minimized_cost}</OBJ>')