import pulp

# Parsing the data
data = {
    'NumShifts': 6, 
    'OfficersNeeded': [15, 13, 11, 11, 9, 7], 
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Problem definition
problem = pulp.LpProblem("Shift_Assignment", pulp.LpMinimize)

# Decision variables
shifts = range(data['NumShifts'])
x = pulp.LpVariable.dicts("Shift", shifts, lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['ShiftCosts'][s] * x[s] for s in shifts)

# Constraints
for s in shifts:
    problem += x[s] + x[(s - 1) % data['NumShifts']] >= data['OfficersNeeded'][s]

# Solve the problem
problem.solve()

# Results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')