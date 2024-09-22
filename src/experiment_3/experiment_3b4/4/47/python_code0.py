import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = {s: pulp.LpVariable(f'x_{s}', lowBound=0, cat='Integer') for s in range(1, data['NumShifts'] + 1)}

# Objective Function
problem += pulp.lpSum(data['ShiftCosts'][s - 1] * x[s] for s in range(1, data['NumShifts'] + 1))

# Constraints
for s in range(1, data['NumShifts'] + 1):
    if s == 1:
        problem += x[s] >= data['OfficersNeeded'][s - 1]
    else:
        problem += x[s] + x[s - 1] >= data['OfficersNeeded'][s - 1]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')