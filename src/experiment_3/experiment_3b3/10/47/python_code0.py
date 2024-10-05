import pulp

# Problem Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Number of shifts
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("PoliceOfficerShiftAssignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective Function
problem += pulp.lpSum(shift_costs[s] * officers_assigned[s] for s in range(S))

# Constraints
# Meeting the requirement for each shift
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s], f"Requirement_{s}"

# Constraints for officers working two consecutive shifts
for s in range(1, S):
    problem += officers_assigned[s] == officers_assigned[s-1], f"Consecutive_{s}"

# Constraint for the first shift
problem += officers_assigned[0] >= officers_needed[0], "First_Shift"

# Solve the problem
problem.solve()

# Print the results
officers_assigned_values = [pulp.value(officers_assigned[s]) for s in range(S)]
print(f'Assigned Officers: {officers_assigned_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')