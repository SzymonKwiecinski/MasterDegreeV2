import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Problem
problem = pulp.LpProblem("Shift_Scheduling", pulp.LpMinimize)

# Variables
x = {s: pulp.LpVariable(f'x_{s}', lowBound=0, cat='Integer') for s in range(data['NumShifts'])}

# Objective Function
problem += pulp.lpSum(data['ShiftCosts'][s] * x[s] for s in range(data['NumShifts']))

# Constraints
for s in range(data['NumShifts']):
    if s == 0:
        problem += x[s] + x[data['NumShifts'] - 1] >= data['OfficersNeeded'][s]
    else:
        problem += x[s] + x[s - 1] >= data['OfficersNeeded'][s]

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')