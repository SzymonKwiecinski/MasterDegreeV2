import pulp

# Problem data
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

# Unpack data
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

# Define the problem
problem = pulp.LpProblem("Seaport_Container_Problem", pulp.LpMinimize)

# Decision variables
unloaded = pulp.LpVariable.dicts("Unloaded", range(T), lowBound=0, cat='Integer')
cranes = pulp.LpVariable.dicts("Cranes", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
stock = pulp.LpVariable.dicts("Stock", range(T+1), lowBound=0, upBound=max_container, cat='Integer')

# Initialize stock at the start
problem += (stock[0] == init_container)

# Stock balance constraints and demand satisfaction
for t in range(T):
    problem += (unloaded[t] <= unload_capacity[t])  # Unloading capacity
    problem += (unloaded[t] + stock[t] >= demands[t] + stock[t + 1])  # Demand satisfaction and stock update
    problem += (stock[t + 1] == stock[t] + unloaded[t] - demands[t])  # Stock balance
    problem += (cranes[t] * crane_capacity >= demands[t])  # Crane capacity meets demand

# Final stock should be zero
problem += stock[T] == 0

# Objective function
total_unload_cost = pulp.lpSum(unload_costs[t] * unloaded[t] for t in range(T))
total_holding_cost = pulp.lpSum(holding_cost * stock[t] for t in range(T))
total_crane_cost = pulp.lpSum(crane_cost * cranes[t] for t in range(T))

problem += total_unload_cost + total_holding_cost + total_crane_cost

# Solve the problem
problem.solve()

# Retrieve result
output = {
    "containers_unloaded": [pulp.value(unloaded[t]) for t in range(T)],
    "cranes_rented": [pulp.value(cranes[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')