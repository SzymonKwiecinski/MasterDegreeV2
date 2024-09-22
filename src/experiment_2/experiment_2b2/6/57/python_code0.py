import pulp

# Data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extract data
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

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
containers_end = pulp.LpVariable.dicts("containers_end", range(T), lowBound=0, cat='Integer')

# LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Objective function
problem += pulp.lpSum([unload_costs[t] * amount[t] for t in range(T)]) + \
           pulp.lpSum([crane_cost * crane[t] for t in range(T)]) + \
           pulp.lpSum([holding_cost * containers_end[t] for t in range(T-1)])

# Constraints

# Initial containers constraint
problem += (init_container + amount[0] == demands[0] + containers_end[0]), "Initial_Containers"

# Monthly constraints
for t in range(T):
    # Unload capacity constraint
    problem += (amount[t] <= unload_capacities[t]), f"Unload_Capacity_{t}"

    # Crane rental constraint: cranes rented x capacity should fulfill demands
    problem += (crane[t] * crane_capacity >= demands[t]), f"Crane_Capacity_{t}"

    # Storage capacity constraint
    problem += (containers_end[t] <= max_container), f"Max_Storage_{t}"

    if t > 0:
        # Balance constraints: containers from the previous end plus current unload equals demand plus current end
        problem += (containers_end[t-1] + amount[t] == demands[t] + containers_end[t]), f"Balance_{t}"

# Yard must be empty at the end of the last month
problem += (containers_end[T-1] == 0), "Final_Containers_Empty"

# Solve the problem
problem.solve()

# Results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [crane[t].varValue for t in range(T)]

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')