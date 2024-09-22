import pulp
import json

# Data from JSON format
data = {'T': 4, 'Demands': [450, 700, 500, 750], 'UnloadCosts': [75, 100, 105, 130], 'UnloadCapacity': [800, 500, 450, 700], 'HoldingCost': 20, 'MaxContainer': 500, 'InitContainer': 200, 'NumCranes': 4, 'CraneCapacity': 200, 'CraneCost': 1000}

# Constants
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

# Initialize the problem
problem = pulp.LpProblem("Seaport_Container_Management", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=UnloadCapacity[t-1], cat='Integer') for t in range(1, T+1)]
hold = [pulp.LpVariable(f'hold_{t}', lowBound=0, upBound=MaxContainer, cat='Integer') for t in range(T+1)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=NumCranes, cat='Integer') for t in range(1, T+1)]

# Objective Function
problem += pulp.lpSum(UnloadCosts[t-1] * amount[t-1] + HoldingCost * hold[t] + CraneCost * crane[t-1] for t in range(1, T+1))

# Constraints
problem += hold[0] == InitContainer  # Initial hold
problem += hold[T] == 0  # No containers should remain after the last month

for t in range(1, T+1):
    problem += amount[t-1] <= UnloadCapacity[t-1]  # Unloading capacity constraint
    problem += crane[t-1] <= NumCranes  # Crane usage constraint
    problem += crane[t-1] * CraneCapacity >= Demands[t-1]  # Crane capacity must meet demand
    if t > 1:
        problem += hold[t] == hold[t-1] + amount[t-1] - Demands[t-1]  # Update hold based on previous month

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')