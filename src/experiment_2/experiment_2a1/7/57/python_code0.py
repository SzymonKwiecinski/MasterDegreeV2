import pulp
import json

# Data input
data = json.loads('{"T": 4, "Demands": [450, 700, 500, 750], "UnloadCosts": [75, 100, 105, 130], "UnloadCapacity": [800, 500, 450, 700], "HoldingCost": 20, "MaxContainer": 500, "InitContainer": 200, "NumCranes": 4, "CraneCapacity": 200, "CraneCost": 1000}')

# Constants
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

# Problem definition
problem = pulp.LpProblem("Container_Management_Problem", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(T), lowBound=0, upBound=None, cat='Integer')  # Containers unloaded
cranes = pulp.LpVariable.dicts("Cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')  # Cranes rented
inventory = [pulp.LpVariable(f"Inventory_{t}", lowBound=0, upBound=max_container) for t in range(T + 1)]  # Containers in inventory

# Objective function
total_cost = pulp.lpSum([
    unload_costs[t] * amount[t] for t in range(T)
]) + pulp.lpSum([
    holding_cost * inventory[t] for t in range(1, T + 1)
]) + pulp.lpSum([
    crane_cost * cranes[t] for t in range(T)
])

problem += total_cost

# Constraints
problem += inventory[0] == init_container  # Initial inventory
for t in range(T):
    problem += inventory[t] + amount[t] - demands[t] == inventory[t + 1]  # Inventory balance
    problem += amount[t] <= unload_capacity[t]  # Unloading capacity
    problem += amount[t] <= inventory[t] + unload_capacity[t]  # Available containers for unloading

for t in range(T):
    problem += cranes[t] * crane_capacity >= demands[t] - inventory[t]  # Ensure demand is met by cranes

# Final inventory should be zero
problem += inventory[T] == 0

# Solve the problem
problem.solve()

# Collecting results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output results
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')