import pulp

# Given data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 
        'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 
        'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 
        'CraneCapacity': 200, 'CraneCost': 1000}

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

# Create problem
problem = pulp.LpProblem("Seaport_Container_Handling", pulp.LpMinimize)

# Variables
amount = pulp.LpVariable.dicts("Unload", range(T), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("Crane", range(T), lowBound=0, upBound=num_cranes, cat='Integer')
stored = pulp.LpVariable.dicts("Stored", range(T), lowBound=0, upBound=max_container, cat='Integer')

# Objective
total_cost = (
    pulp.lpSum(unload_costs[t] * amount[t] for t in range(T)) + 
    pulp.lpSum(holding_cost * stored[t] for t in range(T)) +
    pulp.lpSum(crane_cost * crane[t] for t in range(T))
)
problem += total_cost

# Constraints
# Initial conditions
problem += stored[0] == init_container + amount[0] - demands[0]

# Monthly constraints
for t in range(T):
    problem += amount[t] <= unload_capacity[t]
    problem += crane[t] * crane_capacity >= demands[t]
    if t > 0:
        problem += stored[t] == stored[t-1] + amount[t] - demands[t]

# End condition
problem += stored[T-1] == 0

# Solve problem
problem.solve()

# Output formatting
containers_unloaded = [int(pulp.value(amount[t])) for t in range(T)]
cranes_rented = [int(pulp.value(crane[t])) for t in range(T)]
total_cost_value = pulp.value(total_cost)

output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')