import pulp

# Data from the provided JSON
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

# Initialize the problem
problem = pulp.LpProblem("Seaport_Container_Operations", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f"x_{t}", lowBound=0, upBound=data['UnloadCapacity'][t], cat='Continuous') for t in range(data['T'])]
y = [pulp.LpVariable(f"y_{t}", lowBound=0, upBound=data['NumCranes'], cat='Integer') for t in range(data['T'])]
s = [pulp.LpVariable(f"s_{t}", lowBound=0, upBound=data['MaxContainer'], cat='Continuous') for t in range(data['T'])]

# Objective function
problem += pulp.lpSum(data['UnloadCosts'][t] * x[t] + data['HoldingCost'] * s[t] + data['CraneCost'] * y[t] for t in range(data['T']))

# Initial condition
problem += (s[0] == data['InitContainer'], "Initial_Condition")

# Flow balance constraints
for t in range(data['T']):
    if t == 0:
        problem += (data['InitContainer'] + x[t] == data['Demands'][t] + s[t], f"Flow_Balance_{t}")
    else:
        problem += (s[t-1] + x[t] == data['Demands'][t] + s[t], f"Flow_Balance_{t}")

# Loading requirement constraints
for t in range(data['T']):
    problem += (y[t] * data['CraneCapacity'] >= data['Demands'][t], f"Loading_Requirement_{t}")

# Final condition
problem += (s[data['T']-1] == 0, "Final_Condition")

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')