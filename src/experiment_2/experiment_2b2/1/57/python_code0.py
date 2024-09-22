import pulp

# Data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

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

# Create a linear programming problem
problem = pulp.LpProblem("Seaport_Operation", pulp.LpMinimize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat=pulp.LpInteger) for t in range(T)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat=pulp.LpInteger) for t in range(T)]
yard = [pulp.LpVariable(f'yard_{t}', lowBound=0, upBound=max_container, cat=pulp.LpInteger) for t in range(T)]

# Objective function
problem += pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + \
           pulp.lpSum(crane_cost * crane[t] for t in range(T)) + \
           pulp.lpSum(holding_cost * yard[t] for t in range(T))

# Constraints
problem += yard[0] == init_container + amount[0] - demands[0] - crane[0] * crane_capacity, "Initial_Inventory"
for t in range(1, T):
    problem += yard[t] == yard[t-1] + amount[t] - demands[t] - crane[t] * crane_capacity, f"Inventory_Balance_{t}"
problem += yard[T-1] == 0, "Final_Inventory"

# Solve the problem
problem.solve()

# Extract solutions
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(crane[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output the result
result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')