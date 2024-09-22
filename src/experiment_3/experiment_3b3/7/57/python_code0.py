import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Container_Yard_Optimization", pulp.LpMinimize)

# Variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, cat='Integer')
containers_in_yard = pulp.LpVariable.dicts("containers_in_yard", range(T+1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum([
    unload_costs[t] * amount[t] + holding_cost * containers_in_yard[t] + crane_cost * crane[t]
    for t in range(T)
])

# Constraints
# 1. Demand Fulfillment
problem += pulp.lpSum([amount[t] for t in range(T)]) >= pulp.lpSum(demands)

# 2. Unloading Capacity
for t in range(T):
    problem += amount[t] <= unload_capacity[t]

# 3. Yard Capacity
for t in range(T):
    problem += containers_in_yard[t] <= max_container

# 4. Number of Cranes
for t in range(T):
    problem += crane[t] <= num_cranes

# 5. Crane Loading Capacity
for t in range(T):
    problem += crane[t] * crane_capacity >= demands[t]

# 6. Containers in Yard Calculation
for t in range(T-1):
    problem += containers_in_yard[t+1] == containers_in_yard[t] + amount[t] - demands[t]

# 7. Initial Condition
problem += containers_in_yard[0] == init_container

# 8. Final Condition
problem += containers_in_yard[T] == 0

# Solve
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')