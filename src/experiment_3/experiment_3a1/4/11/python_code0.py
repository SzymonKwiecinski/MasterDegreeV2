import pulp
import json

# Data input in JSON format
data = json.loads("{'T': 12, 'Deliver': [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], 'StorageCost': 5, 'SwitchCost': 10}")

# Extracting parameters
T = data['T']
deliveries = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Production", range(1, T + 1), lowBound=0, cat='Continuous')  # Production variables
I = pulp.LpVariable.dicts("Inventory", range(1, T + 1), lowBound=0, cat='Continuous')  # Inventory variables

# Objective Function
problem += pulp.lpSum(storage_cost * I[i] for i in range(1, T + 1)) + \
           pulp.lpSum(switch_cost * pulp.lpAbs(x[i + 1] - x[i]) for i in range(1, T)), "Total_Cost"

# Constraints

# Inventory Balance and initial condition
problem += I[1] == x[1] - deliveries[0], "Inventory_Balance_1"
for i in range(2, T + 1):
    problem += I[i] == I[i - 1] + x[i] - deliveries[i - 1], f"Inventory_Balance_{i}"

# Ensure the inventory at the end of the year has no value
problem += I[T] == 0, "No_Inventory_End_Year"

# Solve the problem
problem.solve()

# Output the production schedule and total cost
productions = [x[i].varValue for i in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Productions: {productions}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')