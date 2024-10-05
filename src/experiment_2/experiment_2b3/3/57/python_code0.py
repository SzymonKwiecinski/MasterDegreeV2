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

# Unpacking data
T = data['T']
Demands = data['Demands']
UnloadCosts = data['UnloadCosts']
UnloadCapacity = data['UnloadCapacity']
HoldingCost = data['HoldingCost']
MaxContainer = data['MaxContainer']
InitContainer = data['InitContainer']
NumCranes = data['NumCranes']
CraneCapacity = data['CraneCapacity']
CraneCost = data['CraneCost']

# Problem
problem = pulp.LpProblem("Seaport_Operation", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=NumCranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T+1), lowBound=0, cat='Integer')

# Initial inventory constraint
problem += inventory[0] == InitContainer

# Objective function
problem += pulp.lpSum(
    UnloadCosts[t] * amount[t] + CraneCost * crane[t] + HoldingCost * inventory[t+1]
    for t in range(T)
)

# Constraints
for t in range(T):
    # Unloading capacity
    problem += amount[t] <= UnloadCapacity[t]

    # Crane capacity constraint
    problem += crane[t] * CraneCapacity >= Demands[t]

    # Inventory balance
    problem += inventory[t+1] == inventory[t] + amount[t] - Demands[t]

    # Maximum storage capacity
    problem += inventory[t+1] <= MaxContainer

# End of planning period inventory
problem += inventory[T] == 0

# Solve problem
problem.solve()

# Output
output = {
    "containers_unloaded": [pulp.value(amount[t]) for t in range(T)],
    "cranes_rented": [pulp.value(crane[t]) for t in range(T)],
    "total_cost": pulp.value(problem.objective)
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')