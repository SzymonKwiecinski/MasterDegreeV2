import pulp
import json

# Input data
data = json.loads('{"T": 4, "Demands": [450, 700, 500, 750], "UnloadCosts": [75, 100, 105, 130], "UnloadCapacity": [800, 500, 450, 700], "HoldingCost": 20, "MaxContainer": 500, "InitContainer": 200, "NumCranes": 4, "CraneCapacity": 200, "CraneCost": 1000}')

# Define the time horizon
T = data['T']

# Create the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Unload", range(1, T + 1), lowBound=0, cat='Integer')  # x_t
y = pulp.LpVariable.dicts("Cranes", range(1, T + 1), lowBound=0, upBound=data['NumCranes'], cat='Integer')  # y_t
s = pulp.LpVariable.dicts("Storage", range(1, T + 1), lowBound=0, upBound=data['MaxContainer'], cat='Integer')  # s_t

# Objective function
problem += pulp.lpSum(data['UnloadCosts'][t - 1] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(1, T + 1)), "Total_Cost"

# Constraints
# Unloading and storage dynamics
s[0] = data['InitContainer']  # s_0
for t in range(1, T + 1):
    problem += s[t-1] + x[t] == data['Demands'][t - 1] + s[t], f"Storage_Dynamics_{t}"

# Unloading capacity
for t in range(1, T + 1):
    problem += x[t] <= data['UnloadCapacity'][t - 1], f"Unload_Capacity_{t}"

# Crane capacity
for t in range(1, T + 1):
    problem += data['Demands'][t - 1] <= data['CraneCapacity'] * y[t], f"Crane_Capacity_{t}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')