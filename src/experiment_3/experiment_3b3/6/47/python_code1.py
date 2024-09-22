import pulp

# Problem data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Extract data elements
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Initialize the problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts(
    "OfficersAssigned", range(S), lowBound=0, cat=pulp.LpInteger)

# Objective function
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] // 2 + (officers_assigned[s] % 2)) for s in range(S))

# Constraints
# For the first shift
problem += officers_assigned[0] >= officers_needed[0]

# For subsequent shifts
for s in range(1, S):
    problem += officers_assigned[s] + officers_assigned[s - 1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Results
for s in range(S):
    print(f'Shift {s+1}: Assigned Officers = {pulp.value(officers_assigned[s])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')