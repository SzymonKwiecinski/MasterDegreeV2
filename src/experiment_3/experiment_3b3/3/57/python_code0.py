import pulp

# Data
data = {
    "T": 4,
    "Demands": [450, 700, 500, 750],
    "UnloadCosts": [75, 100, 105, 130],
    "UnloadCapacity": [800, 500, 450, 700],
    "HoldingCost": 20,
    "MaxContainer": 500,
    "InitContainer": 200,
    "NumCranes": 4,
    "CraneCapacity": 200,
    "CraneCost": 1000
}

# Constants
T = data["T"]
Demands = data["Demands"]
UnloadCosts = data["UnloadCosts"]
UnloadCapacity = data["UnloadCapacity"]
HoldingCost = data["HoldingCost"]
MaxContainer = data["MaxContainer"]
InitContainer = data["InitContainer"]
NumCranes = data["NumCranes"]
CraneCapacity = data["CraneCapacity"]
CraneCost = data["CraneCost"]

# Problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = pulp.LpVariable.dicts("amount", (t for t in range(T)), lowBound=0, cat='Continuous')
crane = pulp.LpVariable.dicts("crane", (t for t in range(T)), lowBound=0, upBound=NumCranes, cat='Integer')
inventory = pulp.LpVariable.dicts("inventory", (t for t in range(T + 1)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(
    UnloadCosts[t] * amount[t] + HoldingCost * inventory[t] + CraneCost * crane[t]
    for t in range(T)
)

# Constraints
# Initial inventory
problem += inventory[0] == InitContainer

# Inventory balance and other constraints
for t in range(T):
    problem += inventory[t] + amount[t] - Demands[t] == inventory[t + 1]
    problem += inventory[t] <= MaxContainer
    problem += amount[t] <= UnloadCapacity[t]
    problem += crane[t] * CraneCapacity >= Demands[t] - (inventory[t] if t == 0 else inventory[t - 1])

# End inventory
problem += inventory[T] == 0

# Solve
problem.solve()

# Output
amounts_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [crane[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

print(f"Containers Unloaded: {amounts_unloaded}")
print(f"Cranes Rented: {cranes_rented}")
print(f"Total Cost (Objective Value): <OBJ>{total_cost}</OBJ>")