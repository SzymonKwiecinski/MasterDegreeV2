import pulp
import json

# Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Problem parameters
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

# Create the LP problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Integer') for t in range(T)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
inventory = [pulp.LpVariable(f'inventory_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T + 1)]

# Constraints
inventory[0] = init_container  # Initial inventory

for t in range(T):
    if t > 0:
        inventory[t] = inventory[t-1] + amount[t-1] - demands[t-1]
    # Ensure inventory does not exceed maximum capacity
    problem += inventory[t] <= max_container
    # Unloading capacity constraint
    problem += amount[t] <= unload_capacity[t]
    # Calculate how many containers can be loaded with rented cranes
    problem += amount[t] <= crane[t] * crane_capacity

# Last month inventory should be 0
problem += inventory[T] == 0

# Objective function
total_cost = pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + \
             pulp.lpSum(holding_cost * inventory[t] for t in range(T)) + \
             pulp.lpSum(crane_cost * crane[t] for t in range(T))

problem += total_cost

# Solve the problem
problem.solve()

# Output the results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [crane[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')