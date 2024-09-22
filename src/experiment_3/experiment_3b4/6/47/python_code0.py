import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

NumShifts = data['NumShifts']
OfficersNeeded = data['OfficersNeeded']
ShiftCosts = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("OfficerScheduling", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Integer') for s in range(NumShifts)]

# Objective
problem += pulp.lpSum(ShiftCosts[s] * x[s] for s in range(NumShifts))

# Constraints
for s in range(NumShifts):
    problem += x[s] + x[(s - 1) % NumShifts] >= OfficersNeeded[s]

# Solve
problem.solve()

# Print Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')