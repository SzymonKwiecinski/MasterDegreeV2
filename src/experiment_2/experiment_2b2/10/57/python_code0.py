import pulp

# Extract data from the JSON format
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
problem = pulp.LpProblem("Seaport_Container_Problem", pulp.LpMinimize)

# Decision variables
unload_amount = pulp.LpVariable.dicts("UnloadAmount", range(T), lowBound=0, upBound=None, cat=pulp.LpInteger)
cranes_used = pulp.LpVariable.dicts("CranesUsed", range(T), lowBound=0, upBound=num_cranes, cat=pulp.LpInteger)
yard_containers = pulp.LpVariable.dicts("YardContainers", range(T+1), lowBound=0, upBound=max_container, cat=pulp.LpInteger)

# Objective function
problem += (
    pulp.lpSum(unload_costs[t] * unload_amount[t] for t in range(T)) 
    + pulp.lpSum(crane_cost * cranes_used[t] for t in range(T)) 
    + pulp.lpSum(holding_cost * yard_containers[t+1] for t in range(T))
)

# Constraints
problem += yard_containers[0] == init_container, "InitialContainers"

for t in range(T):
    problem += unload_amount[t] <= unload_capacity[t], f"UnloadCapacity_{t}"
    problem += cranes_used[t] * crane_capacity >= demands[t], f"CraneDemand_{t}"
    problem += yard_containers[t] + unload_amount[t] - demands[t] == yard_containers[t+1], f"Balance_{t}"

problem += yard_containers[T] == 0, "FinalEmptyYard"

# Solve the problem
problem.solve()

# Collecting results
containers_unloaded = [pulp.value(unload_amount[t]) for t in range(T)]
cranes_rented = [pulp.value(cranes_used[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

result = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')