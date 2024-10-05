import pulp

# Extract data from JSON
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

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
problem = pulp.LpProblem("Seaport_Container_Transport", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("Amount", range(T), lowBound=0, cat=pulp.LpInteger)
cranes = pulp.LpVariable.dicts("Cranes", range(T), lowBound=0, cat=pulp.LpInteger)
storage = pulp.LpVariable.dicts("Storage", range(T), lowBound=0, cat=pulp.LpInteger)

# Objective function
unload_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)])
crane_costs = pulp.lpSum([cranes[t] * crane_cost for t in range(T)])
holding_costs = pulp.lpSum([holding_cost * storage[t] for t in range(T)])

problem += unload_cost + crane_costs + holding_costs

# Constraints

# Initial storage condition
problem += storage[0] == init_container + amount[0] - demands[0]

# Monthly constraints
for t in range(T):
    # Demand fulfillment
    problem += demands[t] <= cranes[t] * crane_capacity

    # Unloading capacity
    problem += amount[t] <= unload_capacity[t]

    # Maximum number of cranes rented
    problem += cranes[t] <= num_cranes

    # Storage capacity
    problem += storage[t] <= max_container

    if t < T - 1:
        # Update storage for next month
        problem += storage[t + 1] == storage[t] + amount[t + 1] - demands[t + 1]

# Final month storage should be zero
problem += storage[T - 1] == 0

# Solve the problem
problem.solve()

# Retrieve results
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Format the output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')