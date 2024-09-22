import pulp
import json

# Input data
data = {'T': 4, 
        'Demands': [450, 700, 500, 750], 
        'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 
        'HoldingCost': 20, 
        'MaxContainer': 500, 
        'InitContainer': 200, 
        'NumCranes': 4, 
        'CraneCapacity': 200, 
        'CraneCost': 1000}

# Problem setup
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

# Create the linear programming problem
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision variables
amount_t = pulp.LpVariable.dicts("amount_t", range(T), lowBound=0, cat='Continuous')
crane_t = pulp.LpVariable.dicts("crane_t", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
hold_t = pulp.LpVariable.dicts("hold_t", range(T+1), lowBound=0, upBound=max_container, cat='Continuous')

# Initial condition
hold_t[0] = init_container

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amount_t[t] + holding_cost * hold_t[t] + crane_cost * crane_t[t] 
                          for t in range(T)])
problem += total_cost

# Constraints
for t in range(T):
    # Demand satisfaction
    problem += hold_t[t] + amount_t[t] - demands[t] == hold_t[t + 1], f"demand_satisfaction_{t}"
    
    # Unload capacity
    problem += amount_t[t] <= unload_capacity[t], f"unload_capacity_{t}"
    
    # Crane capacity
    problem += crane_t[t] * crane_capacity >= demands[t] - hold_t[t], f"crane_capacity_{t}"

# Last month constraint: no containers should remain
problem += hold_t[T] == 0, "final_storage_zero"

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount_t[t].varValue for t in range(T)]
cranes_rented = [crane_t[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')