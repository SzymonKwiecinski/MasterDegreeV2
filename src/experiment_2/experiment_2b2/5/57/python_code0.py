import pulp

# Parse the input data
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
Demands = data['Demands']
UnloadCosts = data['UnloadCosts']
UnloadCapacity = data['UnloadCapacity']
HoldingCost = data['HoldingCost']
MaxContainer = data['MaxContainer']
InitContainer = data['InitContainer']
NumCranes = data['NumCranes']
CraneCapacity = data['CraneCapacity']
CraneCost = data['CraneCost']

# Create the problem
problem = pulp.LpProblem("Minimize_Seaport_Operation_Costs", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Integer')
crane = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=NumCranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", range(T + 1), lowBound=0, upBound=MaxContainer, cat='Integer')

# Objective function
problem += pulp.lpSum(
    (UnloadCosts[t] * amount[t]) + 
    (CraneCost * crane[t]) + 
    (HoldingCost * inventory[t + 1]) 
    for t in range(T)
), "TotalCost"

# Initial inventory constraint
problem += inventory[0] == InitContainer, "Initial_Inventory"

# Balance constraints for each month
for t in range(T):
    problem += (inventory[t] + amount[t] - Demands[t] - inventory[t + 1] == 0), f"Balance_Constraint_{t}"

# Unloading capacity constraints
for t in range(T):
    problem += amount[t] <= UnloadCapacity[t], f"Unloading_Capacity_{t}"

# Shipping capacity constraints due to cranes
for t in range(T):
    problem += Demands[t] <= crane[t] * CraneCapacity, f"Crane_Capacity_{t}"

# Final inventory must be zero
problem += inventory[T] == 0, "Final_Inventory_Zero"

# Solve the problem
problem.solve()

# Retrieve results
containers_unloaded = [pulp.value(amount[t]) for t in range(T)]
cranes_rented = [pulp.value(crane[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')