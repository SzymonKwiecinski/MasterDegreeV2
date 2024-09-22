import pulp
import json

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Problem Initialization
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

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, upBound=None, cat='Integer')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
holding = pulp.LpVariable.dicts("holding", range(T + 1), lowBound=0, upBound=max_container, cat='Integer')

# Objective Function
total_cost = pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
             pulp.lpSum([holding_cost * holding[t] for t in range(T)]) + \
             pulp.lpSum([crane_cost * cranes[t] for t in range(T)])

problem += total_cost

# Constraints
# Initial condition
problem += holding[0] == init_container

# Demand fulfillment and capacity constraints
for t in range(T):
    problem += amount[t] <= unload_capacity[t], f"UnloadCapacity_{t}"
    problem += holding[t] + amount[t] - demands[t] == holding[t + 1], f"DemandFulfillment_{t}"
    problem += holding[t + 1] <= max_container, f"MaxContainer_{t+1}"
    
# Crane capacity constraints
for t in range(T):
    problem += cranes[t] * crane_capacity >= demands[t] - holding[t], f"CranesCapacity_{t}"

# Solve the problem
problem.solve()

# Extracting the results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')