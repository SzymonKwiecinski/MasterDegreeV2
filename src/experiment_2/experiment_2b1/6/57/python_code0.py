import pulp
import json

# Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 
        'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 
        'HoldingCost': 20, 
        'MaxContainer': 500, 
        'InitContainer': 200, 
        'NumCranes': 4, 
        'CraneCapacity': 200, 
        'CraneCost': 1000}

# Extract data
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
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')  # Containers unloaded each month
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')  # Cranes rented each month
storage = pulp.LpVariable.dicts("storage", range(T+1), lowBound=0, upBound=max_container, cat='Integer')  # Containers in storage

# Initial storage
storage[0] = init_container

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * storage[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += (storage[t] + amount[t] - demands[t] == storage[t+1]), f"Demand_satisfaction_{t}"
    
    # Unloading capacity constraints
    problem += (amount[t] <= unload_capacity[t]), f"Unloading_capacity_{t}"
    
    # Storage capacity constraint
    problem += (storage[t] <= max_container), f"Storage_capacity_{t}"
    
    # Loading constraints based on cranes
    problem += (cranes[t] * crane_capacity >= demands[t] - storage[t]), f"Cranes_usage_{t}"

# Final storage constraint (should be zero)
problem += (storage[T] == 0), "Final_storage_zero"

# Solve the problem
problem.solve()

# Collect results
containers_unloaded = [int(amount[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output the results
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')