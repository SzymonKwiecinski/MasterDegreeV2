import pulp
import json

# Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extracting parameters
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
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Continuous') for t in range(T)]
cranes = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
initial_yard = init_container

# Container storage at the end of each month
storage = [pulp.LpVariable(f'storage_{t}', lowBound=0, upBound=max_container, cat='Continuous') for t in range(T + 1)]
storage[0] = initial_yard  # Initial storage

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * storage[t+1] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += storage[t] + amount[t] - (demands[t] + (storage[t + 1] if t + 1 < T else 0)) == 0, f'Demand_Satisfaction_{t}'
    
    # Crane loading capacity
    problem += cranes[t] * crane_capacity >= demands[t], f'Crane_Capacity_{t}'
    
    # Update storage for next month
    if t < T - 1:
        problem += storage[t + 1] == storage[t] + amount[t] - demands[t], f'Storage_Update_{t}'

# Ensure we end with no containers
problem += storage[T] == 0, 'End_Storage'

# Solve the problem
problem.solve()

# Prepare results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')