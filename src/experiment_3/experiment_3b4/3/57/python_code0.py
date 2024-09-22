import pulp

# Data from the JSON format
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
Demands = data['Demands']
UnloadCosts = data['UnloadCosts']
UnloadCapacity = data['UnloadCapacity']
HoldingCost = data['HoldingCost']
MaxContainer = data['MaxContainer']
InitContainer = data['InitContainer']
NumCranes = data['NumCranes']
CraneCapacity = data['CraneCapacity']
CraneCost = data['CraneCost']

# Problem definition
problem = pulp.LpProblem("Seaport_Operations", pulp.LpMinimize)

# Decision Variables
amount = [pulp.LpVariable(f'amount_{t}', lowBound=0, upBound=UnloadCapacity[t], cat='Continuous') for t in range(T)]
crane = [pulp.LpVariable(f'crane_{t}', lowBound=0, upBound=NumCranes, cat='Integer') for t in range(T)]
hold = [pulp.LpVariable(f'hold_{t}', lowBound=0, upBound=MaxContainer, cat='Continuous') for t in range(T + 1)]

# Objective Function
problem += pulp.lpSum(UnloadCosts[t] * amount[t] + HoldingCost * hold[t] + CraneCost * crane[t] for t in range(T))

# Constraints
# (1) Unloading capacity constraint
# Already handled by the variable bounds

# (2) Holding capacity constraint
# Already handled by the variable bounds

# (3) Demand fulfillment constraint
problem += hold[0] == InitContainer  # Initial condition
for t in range(T):
    problem += amount[t] + hold[t] == Demands[t] + hold[t + 1]

# (4) Ending condition (no containers left)
problem += hold[T] == 0

# (5) Crane usage constraint
for t in range(T):
    problem += Demands[t] <= crane[t] * CraneCapacity

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')