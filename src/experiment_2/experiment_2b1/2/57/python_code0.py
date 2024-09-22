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

# Problem parameters
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

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
holding = pulp.LpVariable.dicts("holding", range(T), lowBound=0, cat='Integer')
cranes_rented = pulp.LpVariable.dicts("cranes_rented", range(T), lowBound=0, upBound=num_cranes, cat='Integer')

# Objective function
total_cost = pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + \
             pulp.lpSum(holding_cost * holding[t] for t in range(T)) + \
             pulp.lpSum(crane_cost * cranes_rented[t] for t in range(T))

problem += total_cost

# Constraints

# Demand fulfillment
for t in range(T):
    if t == 0:
        problem += amount[t] + init_container >= demands[t] + holding[t], f"Demand_Constraint_{t}"
    else:
        problem += amount[t] + holding[t-1] >= demands[t] + holding[t], f"Demand_Constraint_{t}"

# Unloading capacity
for t in range(T):
    problem += amount[t] <= unload_capacities[t], f"Unload_Capacity_Constraint_{t}"

# Maximum containers in the yard
for t in range(T):
    problem += holding[t] <= max_container, f"Max_Container_Constraint_{t}"

# Crane rental capacity
for t in range(T):
    problem += cranes_rented[t] * crane_capacity >= demands[t] + holding[t-1] - holding[t] if t > 0 else cranes_rented[t] * crane_capacity >= demands[t] - holding[t], f"Cranes_Capacity_Constraint_{t}"

# Container should be 0 at the end of the last month
problem += holding[T-1] == 0, "Final_Container_Constraint"

# Solve the problem
problem.solve()

# Results
containers_unloaded = [int(amount[t].varValue) for t in range(T)]
cranes_rented_list = [int(cranes_rented[t].varValue) for t in range(T)]
total_cost_value = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented_list,
    "total_cost": total_cost_value
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')