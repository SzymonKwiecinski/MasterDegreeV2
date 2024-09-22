import pulp
import json

# Load data from JSON format
data = json.loads('{"T": 12, "Deliver": [100, 120, 110, 130, 150, 100, 90, 110, 95, 125, 130, 100], "StorageCost": 5, "SwitchCost": 10}')

# Parameters
T = data['T']
deliver = data['Deliver']
storage_cost = data['StorageCost']
switch_cost = data['SwitchCost']

# Create the linear programming problem
problem = pulp.LpProblem("Inventory_Switching_Cost_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(T), lowBound=0, cat='Continuous')  # Production variables
I = pulp.LpVariable.dicts("I", range(T), lowBound=0, cat='Continuous')  # Inventory variables

# Objective function
problem += pulp.lpSum(storage_cost * I[i] for i in range(T)) + \
           pulp.lpSum(switch_cost * (x[i+1] - x[i]) for i in range(T-1)) + \
           pulp.lpSum(switch_cost * (x[i] - x[i+1]) for i in range(T-1))

# Constraints
problem += I[0] == 0  # Initial inventory constraint

# Inventory update constraints
for i in range(1, T):
    problem += I[i] == I[i-1] + x[i] - deliver[i-1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')