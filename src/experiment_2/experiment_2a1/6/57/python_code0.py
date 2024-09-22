import pulp
import json

# Input data
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

# Extracting data
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
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T + 1), lowBound=0, upBound=max_container, cat='Integer')

# Inventory at the start
inventory[0] = init_container

# Objective function
total_cost = pulp.lpSum([amount[t] * unload_costs[t] for t in range(T)]) + \
              pulp.lpSum([inventory[t] * holding_cost for t in range(T)]) + \
              pulp.lpSum([cranes[t] * crane_cost for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Demand fulfillment and inventory balance
    problem += inventory[t] + amount[t] - demands[t] - inventory[t + 1] == 0, f"Balance_Inventory_{t}"
    # Unloading capacity constraint
    problem += amount[t] <= unload_capacity[t], f"Unload_Capacity_{t}"
    # Maximum inventory constraint
    problem += inventory[t] <= max_container, f"Max_Container_{t}"
    # Crane capacity constraint for loading
    problem += cranes[t] * crane_capacity >= demands[t], f"Crane_Capacity_{t}"

# Inventory at the end of the last month must be 0
problem += inventory[T] == 0, "End_Inventory"

# Solve the problem
problem.solve()

# Prepare the output
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')