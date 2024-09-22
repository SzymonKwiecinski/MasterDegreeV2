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

# Problem definition
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Variables
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

amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
holding = pulp.LpVariable.dicts("holding", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')

# Objective function
total_cost = pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + \
             pulp.lpSum(holding_cost * holding[t] for t in range(T)) + \
             pulp.lpSum(crane_cost * cranes[t] for t in range(T))

problem += total_cost

# Constraints
for t in range(T):
    if t == 0:
        problem += amount[t] <= unload_capacity[t]
        problem += amount[t] + init_container - demands[t] - holding[t] == 0
    else:
        problem += amount[t] <= unload_capacity[t]
        problem += amount[t] + holding[t-1] - demands[t] - holding[t] == 0
        
    problem += holding[t] <= max_container

    # Crane loading capacity constraint
    problem += cranes[t] * crane_capacity >= demands[t] - (holding[t-1] if t > 0 else init_container)

# Final constraint to ensure no containers are left at the end of the last month
problem += holding[T-1] == 0

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [int(amount[t].varValue) for t in range(T)]
cranes_rented = [int(cranes[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

# Printing the output in the required format
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')