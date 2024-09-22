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

# Problem
problem = pulp.LpProblem("Container_Unloading", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("Amount", range(T), lowBound=0)
hold = pulp.LpVariable.dicts("Hold", range(T+1), lowBound=0, upBound=max_container)
crane = pulp.LpVariable.dicts("Crane", range(T), lowBound=0, upBound=num_cranes)

# Objective Function
problem += pulp.lpSum(unload_costs[t] * amount[t] + holding_cost * hold[t+1] + crane_cost * crane[t] for t in range(T))

# Constraints
problem += hold[0] == init_container
for t in range(T):
    problem += amount[t] + hold[t] - hold[t+1] >= demands[t]
    problem += amount[t] <= unload_capacity[t]
    problem += crane[t] * crane_capacity >= demands[t]
problem += hold[T] == 0

# Solve
problem.solve()

# Objective Value
objective_value = pulp.value(problem.objective)
print(f' (Objective Value): <OBJ>{objective_value}</OBJ>')