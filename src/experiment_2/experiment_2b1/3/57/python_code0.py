import pulp
import json

# Input data
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Extract parameters from the data
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

# Define the problem
problem = pulp.LpProblem("Seaport_Cost_Minimization", pulp.LpMinimize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", range(T), lowBound=0, cat='Continuous')
cranes = pulp.LpVariable.dicts("crane", range(T), lowBound=0, upBound=NumCranes, cat='Integer')
storage = pulp.LpVariable.dicts("storage", range(T+1), lowBound=0, upBound=MaxContainer, cat='Continuous')

# Initial storage condition
storage[0] = InitContainer

# Objective function: Minimize total cost (unloading + holding + crane rental)
problem += (
    pulp.lpSum(UnloadCosts[t] * amount[t] for t in range(T)) +
    pulp.lpSum(HoldingCost * storage[t] for t in range(T)) +
    pulp.lpSum(CraneCost * cranes[t] for t in range(T))
)

# Constraints
for t in range(T):
    # Demand constraint
    problem += amount[t] + storage[t] >= Demands[t], f"Demand_{t}"
    # Unloading capacity constraint
    problem += amount[t] <= UnloadCapacity[t], f"UnloadCapacity_{t}"
    # Storage balance constraint
    if t == 0:
        problem += storage[0] == InitContainer - amount[0] + storage[1], f"StorageBalance_{t}"
    elif t == T - 1:
        problem += storage[t] == amount[t-1] + storage[t-1] - Demands[t-1], f"StorageBalance_{t}"
    else:
        problem += storage[t] == amount[t-1] + storage[t-1] - Demands[t-1], f"StorageBalance_{t}"

    # Crane loading constraint
    problem += cranes[t] * CraneCapacity >= Demands[t] - amount[t], f"CranesCapacity_{t}"

# Solve the problem
problem.solve()

# Extracting results
containers_unloaded = [amount[t].varValue for t in range(T)]
cranes_rented = [cranes[t].varValue for t in range(T)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "containers_unloaded": containers_unloaded,
    "cranes_rented": cranes_rented,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')