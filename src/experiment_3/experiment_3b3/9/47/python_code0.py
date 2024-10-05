import pulp

# Data from the problem
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Continuous') for s in range(data['NumShifts'])]

# Objective Function
problem += pulp.lpSum(data['ShiftCosts'][s] * officers_assigned[s] for s in range(data['NumShifts'])), "Total_Cost"

# Constraints
for s in range(data['NumShifts'] - 1):
    problem += officers_assigned[s] + officers_assigned[s + 1] >= data['OfficersNeeded'][s], f"Shift_{s}_Coverage"

problem += officers_assigned[data['NumShifts'] - 2] + officers_assigned[data['NumShifts'] - 1] >= data['OfficersNeeded'][data['NumShifts'] - 2], "Last_Shift_Coverage"

# Solve the problem
problem.solve()

# Output
for s in range(data['NumShifts']):
    print(f'Officers assigned to shift {s + 1}: {pulp.value(officers_assigned[s])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')