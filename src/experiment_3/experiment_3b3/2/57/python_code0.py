import pulp

# Data
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
demand = data['Demands']
unload_cost = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(T), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("Crane", range(T), lowBound=0, cat='Integer')
inventory = pulp.LpVariable.dicts("Inventory", range(T), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([unload_cost[t] * amount[t] + holding_cost * inventory[t] + crane_cost * crane[t] for t in range(T)])

# Constraints

# Unloading Capacity Constraint
for t in range(T):
    problem += amount[t] <= unload_capacity[t], f"UnloadingCapacityConstraint_{t}"

# Demand Fulfillment Constraint
problem += inventory[0] == init_container + amount[0] - demand[0], "InitialInventoryConstraint"
for t in range(1, T):
    problem += amount[t] + inventory[t-1] - inventory[t] == demand[t], f"DemandFulfillmentConstraint_{t}"

# Yard Capacity Constraint
for t in range(T):
    problem += inventory[t] <= max_container, f"YardCapacityConstraint_{t}"

# Crane Limit Constraint
for t in range(T):
    problem += crane[t] <= num_cranes, f"CraneLimitConstraint_{t}"

# Loading Capacity Constraint
problem += crane[0] * crane_capacity >= demand[0] - init_container, "LoadingCapacityConstraint_0"
for t in range(1, T):
    problem += crane[t] * crane_capacity >= demand[t] - inventory[t-1], f"LoadingCapacityConstraint_{t}"

# Final Inventory Constraint
problem += inventory[T-1] == 0, "FinalInventoryConstraint"

# Solving the problem
problem.solve()

# Output
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(crane[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Print results
print(f'Containers Unloaded: {containers_unloaded}')
print(f'Cranes Rented: {cranes_rented}')
print(f'Total Cost (Objective Value): <OBJ>{total_cost}</OBJ>')