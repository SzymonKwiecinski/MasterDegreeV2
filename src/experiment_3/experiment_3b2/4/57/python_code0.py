import pulp
import json

# Data in json format
data = {
    'T': 4,
    'Demands': [450, 700, 500, 750],
    'UnloadCosts': [75, 100, 105, 130],
    'UnloadCapacity': [800, 500, 450, 700],
    'HoldingCost': 20,
    'MaxContainer': 500,
    'InitContainer': 200,
    'NumCranes': 4,
    'CraneCapacity': 200,
    'CraneCost': 1000
}

# Parameters
T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Container_Unloading_Optimization", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("UnloadContainers", range(1, T + 1), lowBound=0)
y = pulp.LpVariable.dicts("CraneRental", range(1, T + 1), lowBound=0, cat='Integer')
h = pulp.LpVariable.dicts("HeldContainers", range(1, T + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(unload_costs[t-1] * x[t] + crane_cost * y[t] + holding_cost * h[t] for t in range(1, T + 1)), "Total_Cost"

# Constraints
# Unloading capacity
for t in range(1, T + 1):
    problem += x[t] <= unload_capacity[t - 1], f"UnloadCapacity_t{t}"

# Initial Balance
problem += h[1] == x[1] + init_container - demands[0], "Init_Balance"

# Balance for subsequent months
for t in range(2, T + 1):
    problem += h[t] == x[t] + h[t - 1] - demands[t - 1], f"Balance_t{t}"

# Maximum storage capacity
for t in range(1, T + 1):
    problem += h[t] <= max_container, f"MaxStorage_t{t}"

# Crane capacity constraints
for t in range(1, T + 1):
    problem += y[t] * crane_capacity >= demands[t - 1], f"CraneCapacity_t{t}"

# Maximum cranes
for t in range(1, T + 1):
    problem += y[t] <= num_cranes, f"MaxCranes_t{t}"

# End balance
problem += h[T] == 0, "End_Balance"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')