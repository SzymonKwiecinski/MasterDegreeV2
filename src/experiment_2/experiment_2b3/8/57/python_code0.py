import pulp

# Load data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Decision variables
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

# Initialize the LP problem
problem = pulp.LpProblem("Seaport_Container_Planning", pulp.LpMinimize)

# Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=unload_capacity[t], cat='Integer') for t in range(T)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=num_cranes, cat='Integer') for t in range(T)]
yard = [pulp.LpVariable(f'yard_{t}', lowBound=0, upBound=max_container, cat='Integer') for t in range(T + 1)]

# Constraints
problem += (yard[0] == init_container, "Initial_Container")

for t in range(T):
    # Fulfill demand
    problem += (amount[t] + yard[t] - demands[t] - crane[t] * crane_capacity == yard[t + 1], f"Balance_{t}")
    # End of period constraint
    if t == T - 1:
        problem += (yard[t + 1] == 0, "End_Container")

# Objective function: Minimize total cost
unload_cost = pulp.lpSum(unload_costs[t] * amount[t] for t in range(T))
holding_cost_total = pulp.lpSum(holding_cost * yard[t] for t in range(T))
crane_rent_cost = pulp.lpSum(crane_cost * crane[t] for t in range(T))

problem += unload_cost + holding_cost_total + crane_rent_cost

# Solve problem
problem.solve()

# Output results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [crane[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')