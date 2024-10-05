import pulp

# Data from the problem
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Create the problem variable to contain the problem data
problem = pulp.LpProblem("ShiftScheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Continuous') for s in range(data['NumShifts'])]

# Objective function
problem += pulp.lpSum(data['ShiftCosts'][s] * x[s] for s in range(data['NumShifts'])), "TotalCost"

# Constraints
for s in range(data['NumShifts']):
    problem += x[s] + x[(s + 1) % data['NumShifts']] >= data['OfficersNeeded'][s], f"DemandConstraint_{s}"

# Solve the problem
problem.solve()

# Print the objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')