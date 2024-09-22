import pulp
import json

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extracting the data from the JSON format
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
problem = pulp.LpProblem("Seaport_Cost_Minimization", pulp.LpMinimize)

# Decision Variables
amounts = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Continuous') for t in range(T)]
cranes = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
holdings = [pulp.LpVariable(f'holding_{t}', lowBound=0, upBound=max_container, cat='Continuous') for t in range(T)]

# Objective function
total_cost = pulp.lpSum([unload_costs[t] * amounts[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * holdings[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])

problem += total_cost

# Constraints
# Demand fulfillment and holding containers for the next month
for t in range(T):
    if t == 0:
        problem += amounts[t] + init_container - holdings[t] == demands[t], f'demand_fulfillment_{t}'
    else:
        problem += amounts[t] + holdings[t-1] - holdings[t] == demands[t], f'demand_fulfillment_{t}'

# Maximum holding constraints
for t in range(T):
    problem += holdings[t] <= max_container, f'max_holding_{t}'

# Crane capacity usage
for t in range(T):
    problem += cranes[t] * crane_capacity >= amounts[t], f'crane_capacity_{t}'

# Solve the problem
problem.solve()

# Collect results
containers_unloaded = [pulp.value(amounts[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes[t]) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output format
result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(result)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')