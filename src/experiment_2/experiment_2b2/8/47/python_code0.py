import pulp

# Data input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
NumShifts = data['NumShifts']
OfficersNeeded = data['OfficersNeeded']
ShiftCosts = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(NumShifts)]

# Objective function
total_cost = pulp.lpSum([ShiftCosts[s] * officers_assigned[s] for s in range(NumShifts)])
problem += total_cost

# Constraints
for s in range(NumShifts):
    problem += officers_assigned[s] + officers_assigned[(s + 1) % NumShifts] >= OfficersNeeded[s]

# Solve the problem
problem.solve()

# Output the results
result = {
    "officers_assigned": [pulp.value(officers_assigned[s]) for s in range(NumShifts)],
    "total_cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')