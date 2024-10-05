import pulp

data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 
        'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extract input data
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
problem = pulp.LpProblem("Seaport_Optimization", pulp.LpMinimize)

# Decision variables
amount_unloaded = [pulp.LpVariable(f'amount_unloaded_{t}', lowBound=0, upBound=unload_capacity[t-1], cat='Integer') for t in range(1, T+1)]
containers_in_yard = [pulp.LpVariable(f'containers_in_yard_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(1, T+1)]
cranes_rented = [pulp.LpVariable(f'cranes_rented_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(1, T+1)]

# Objective function
unloading_costs = pulp.lpSum([unload_costs[t-1] * amount_unloaded[t-1] for t in range(1, T+1)])
holding_costs = pulp.lpSum([holding_cost * containers_in_yard[t-1] for t in range(1, T+1)])
crane_costs = pulp.lpSum([crane_cost * cranes_rented[t-1] for t in range(1, T+1)])

problem += unloading_costs + holding_costs + crane_costs, "Total_Cost"

# Constraints

# Initial inventory balance
problem += (init_container + amount_unloaded[0] - cranes_rented[0] * crane_capacity == demands[0] + containers_in_yard[0]), "Initial_Balance"
# Subsequent months inventory balance
for t in range(1, T):
    problem += (containers_in_yard[t-1] + amount_unloaded[t] - cranes_rented[t] * crane_capacity == demands[t] + containers_in_yard[t], f"Balance_{t}")

# Final month must have zero containers
problem += (containers_in_yard[T-1] == 0), "Final_Zero"

# Solve the problem
problem.solve()

# Retrieving the results
containers_unloaded = [amount_unloaded[t].varValue for t in range(T)]
cranes_rented_value = [cranes_rented[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented_value,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')