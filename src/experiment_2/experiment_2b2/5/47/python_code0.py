import pulp

# Data from JSON
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Number of shifts
S = data['NumShifts']

# Requirements
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Shift_Scheduling_Problem", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective function
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(S)])

# Constraints: Must meet the demand for officers in every shift
for s in range(S):
    problem += (officers_assigned[s] + officers_assigned[(s + 1) % S]) >= officers_needed[s]

# Solve the problem
problem.solve()

# Output results
result = {
    "officers_assigned": [int(officers_assigned[s].varValue) for s in range(S)],
    "total_cost": pulp.value(problem.objective)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')