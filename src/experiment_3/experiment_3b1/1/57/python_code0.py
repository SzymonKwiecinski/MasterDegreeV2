import pulp

# Data from JSON
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

# Variables
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

# Define the problem
problem = pulp.LpProblem("ContainerManagement", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", range(1, T + 1), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(1, T + 1), lowBound=0, upBound=num_cranes, cat='Integer')
containers = pulp.LpVariable.dicts("containers", range(1, T + 1), lowBound=0, upBound=max_container, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    unload_costs[t-1] * amount[t] + 
    holding_cost * (containers[t-1] - demands[t-1]) + 
    crane_cost * crane[t] 
    for t in range(1, T + 1)
), "Total Cost"

# Constraints
containers[1] = init_container + amount[1] - demands[0]  # Initial condition for containers
for t in range(2, T + 1):
    problem += containers[t] == containers[t-1] + amount[t] - demands[t-1], f"ContainerBalance_{t}"

for t in range(1, T + 1):
    problem += containers[t] <= max_container, f"MaxContainer_{t}"
    problem += amount[t] <= unload_capacities[t-1], f"UnloadCapacity_{t}"
    problem += amount[t] <= crane[t] * crane_capacity, f"CraneCapacity_{t}"

problem += containers[T] == 0, "FinalContainerBalance"

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')