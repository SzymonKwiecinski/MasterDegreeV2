import pulp
import json

# Input data in JSON format
data = json.loads("{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}")

# Extracting data from JSON
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_and_Inventory", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0)  # Production variables
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0)   # Inventory variables

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(1, T) if x[i+1] - x[i] >= 0) + \
           pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(1, T) if x[i+1] - x[i] < 0), "Total_Cost"

# Constraints
problem += (I[1] + x[1] == deliver[0]), "Flow_Balance_1"
for i in range(2, T + 1):
    problem += (I[i] + x[i] == deliver[i - 1] + I[i - 1]), f"Flow_Balance_{i}"
problem += (I[T] == 0), "No_End_Inventory"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')