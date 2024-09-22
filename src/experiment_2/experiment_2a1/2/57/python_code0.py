import pulp
import json

# Given data in JSON format
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

# Create the problem variable
problem = pulp.LpProblem("Seaport_Operation_Optimization", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')  # containers unloaded each month
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')  # cranes rented each month
inventory = pulp.LpVariable.dicts("inventory", range(T + 1), lowBound=0, upBound=max_container, cat='Continuous')  # containers in yard

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * inventory[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])
problem += total_cost

# Constraints
# Initial inventory
problem += (inventory[0] == init_container)

# Inventory balance and capacity constraints
for t in range(T):
    problem += (inventory[t] + amount[t] - demands[t] == inventory[t + 1], f"Balance_{t}")
    problem += (amount[t] <= unload_capacity[t], f"Unload_Capacity_{t}")
    problem += (inventory[t + 1] <= max_container, f"Max_Container_{t + 1}")

# Crane capacity constraints
for t in range(T):
    problem += (cranes[t] * crane_capacity >= demands[t], f"Cranes_Capacity_{t}")

# Non-negativity and capacity constraints for cranes
for t in range(T):
    problem += (cranes[t] <= num_cranes, f"Max_Cranes_{t}")

# Ending inventory must be zero
problem += (inventory[T] == 0, "End_Inventory")

# Solve the problem
problem.solve()

# Extract results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output results
results = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')