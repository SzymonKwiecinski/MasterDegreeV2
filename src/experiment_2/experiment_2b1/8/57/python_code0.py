import pulp
import json

# Input data in JSON format
data = '{"T": 4, "Demands": [450, 700, 500, 750], "UnloadCosts": [75, 100, 105, 130], "UnloadCapacity": [800, 500, 450, 700], "HoldingCost": 20, "MaxContainer": 500, "InitContainer": 200, "NumCranes": 4, "CraneCapacity": 200, "CraneCost": 1000}'
input_data = json.loads(data)

# Extract variables from input data
T = input_data['T']
demands = input_data['Demands']
unload_costs = input_data['UnloadCosts']
unload_capacity = input_data['UnloadCapacity']
holding_cost = input_data['HoldingCost']
max_container = input_data['MaxContainer']
init_container = input_data['InitContainer']
num_cranes = input_data['NumCranes']
crane_capacity = input_data['CraneCapacity']
crane_cost = input_data['CraneCost']

# Create the LP problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
holding = pulp.LpVariable.dicts("holding", range(T + 1), lowBound=0, upBound=max_container, cat='Integer')

# Objective function: Total costs
total_cost = pulp.lpSum([
    unload_costs[t] * amount[t] for t in range(T)
]) + pulp.lpSum([
    holding_cost * holding[t] for t in range(T + 1)
]) + pulp.lpSum([
    crane_cost * cranes[t] for t in range(T)
])

problem += total_cost

# Constraints
# Initial containers
problem += (holding[0] == init_container)

# Demand satisfaction and holding constraints for each month
for t in range(T):
    problem += (holding[t] + amount[t] - demands[t] == holding[t + 1])
    problem += (amount[t] <= unload_capacity[t])

# Crane loading capacity constraints
for t in range(T):
    problem += (cranes[t] * crane_capacity >= demands[t])

# Non-negativity constraints
for t in range(T):
    problem += (amount[t] >= 0)
    problem += (cranes[t] >= 0)

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

print(output)
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')