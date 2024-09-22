import json
import pulp

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extract data from json
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

# Initialize the problem
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer') # containers unloaded each month
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer') # cranes rented each month
end_containers = pulp.LpVariable.dicts("end_containers", range(T), lowBound=0, cat='Integer') # containers at end of month

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * end_containers[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * crane[t] for t in range(T)])

problem += total_cost

# Constraints
for t in range(T):
    # Demand fulfillment
    if t == 0:
        problem += amount[t] + init_container - end_containers[t] == demands[t]
    else:
        problem += amount[t] + end_containers[t-1] - end_containers[t] == demands[t]
    
    # Unloading capacity
    problem += amount[t] <= unload_capacity[t]
    
    # Crane loading capacity
    problem += crane[t] * crane_capacity >= demands[t]
    
    # End containers capacity
    problem += end_containers[t] <= max_container
    
    # Update for the first month
    if t == 0:
        problem += end_containers[t] >= 0

# Final condition
problem += end_containers[T-1] == 0

# Solve the problem
problem.solve()

# Gather results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [crane[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')