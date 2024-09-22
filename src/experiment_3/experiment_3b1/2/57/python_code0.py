import pulp

# Data from JSON format
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

T = data['T']
demands = data['Demands']
unload_costs = data['UnloadCosts']
unload_capacities = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amounts = pulp.LpVariable.dicts("Amount", range(T), lowBound=0)
cranes = pulp.LpVariable.dicts("Crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
storages = pulp.LpVariable.dicts("Storage", range(T+1), lowBound=0, upBound=max_container)

# Initial storage
storages[0] = init_container

# Objective Function
problem += pulp.lpSum(unload_costs[t] * amounts[t] + holding_cost * storages[t] + crane_cost * cranes[t] for t in range(T))

# Constraints
for t in range(T):
    # Unloading Constraint
    problem += amounts[t] <= unload_capacities[t]
    
    # Demand Fulfillment
    if t > 0:
        problem += demands[t] <= amounts[t] + storages[t-1]
    else:
        problem += demands[t] <= amounts[t] + storages[0]
    
    # Storage Capacity
    problem += storages[t] <= max_container
    
    # Crane Constraint
    problem += cranes[t] * crane_capacity >= demands[t] - (storages[t-1] if t > 0 else 0)

# Final Storage Constraint
problem += storages[T] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')