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
demand = data['Demands']
unload_cost = data['UnloadCosts']
unload_capacity = data['UnloadCapacity']
holding_cost = data['HoldingCost']
max_container = data['MaxContainer']
init_container = data['InitContainer']
num_cranes = data['NumCranes']
crane_capacity = data['CraneCapacity']
crane_cost = data['CraneCost']

# Problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Unload", range(1, T + 1), lowBound=0, cat='Integer')
y = pulp.LpVariable.dicts("Cranes", range(1, T + 1), lowBound=0, cat='Integer')
s = pulp.LpVariable.dicts("Storage", range(1, T + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(unload_cost[t-1] * x[t] + holding_cost * s[t] + crane_cost * y[t] for t in range(1, T + 1))

# Constraints
for t in range(1, T + 1):
    problem += x[t] <= unload_capacity[t-1]
    problem += s[t] <= max_container
    if t == 1:
        problem += x[t] + init_container - s[t] == demand[t-1]
    else:
        problem += x[t] + s[t-1] - s[t] == demand[t-1]
    problem += y[t] * crane_capacity >= demand[t-1]
    problem += y[t] <= num_cranes

problem += s[T] == 0

# Solve the problem
problem.solve()

# Output the results
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")