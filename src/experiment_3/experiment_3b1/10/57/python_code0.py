import pulp
import json

# Data input
data = json.loads('{"T": 4, "Demands": [450, 700, 500, 750], "UnloadCosts": [75, 100, 105, 130], "UnloadCapacity": [800, 500, 450, 700], "HoldingCost": 20, "MaxContainer": 500, "InitContainer": 200, "NumCranes": 4, "CraneCapacity": 200, "CraneCost": 1000}')

# Parameters
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

# Problem definition
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
held = pulp.LpVariable.dicts("held", range(1, T + 1), lowBound=0, upBound=max_container, cat='Continuous')

# Objective Function
problem += pulp.lpSum([unload_costs[t - 1] * amount[t] for t in range(1, T + 1)]) + \
           pulp.lpSum([holding_cost * held[t] for t in range(1, T + 1)]) + \
           pulp.lpSum([crane_cost * crane[t] for t in range(1, T + 1)])

# Constraints
# Unloading capacity constraint
for t in range(1, T + 1):
    problem += amount[t] <= unload_capacity[t - 1]

# Holding constraints
problem += held[1] == init_container + amount[1] - demands[0]
for t in range(2, T + 1):
    problem += held[t] == held[t - 1] + amount[t] - demands[t - 1]

# Max container constraint
for t in range(1, T + 1):
    problem += held[t] <= max_container

# Crane capacity constraint
problem += pulp.lpSum([crane[t] * crane_capacity for t in range(1, T + 1)]) >= pulp.lpSum(demands)

# Last month holding constraint
problem += held[T] == 0

# Solve the problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(1, T + 1)]
cranes_rented = [crane[t].varValue for t in range(1, T + 1)]
total_cost = pulp.value(problem.objective)

print(f'Containers Unloaded: {containers_unloaded}')
print(f'Crane Rented: {cranes_rented}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')