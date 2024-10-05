import pulp

data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extracting data
NumShifts = data['NumShifts']
OfficersNeeded = data['OfficersNeeded']
ShiftCosts = data['ShiftCosts']

# Defining the Linear Programming problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

# Decision variables: Number of officers starting at each shift
officers_starting = [pulp.LpVariable(f"officers_starting_{s}", lowBound=0, cat='Integer') for s in range(NumShifts)]

# Objective function: Minimize the total cost of assigning officers
problem += pulp.lpSum([ShiftCosts[s] * officers_starting[s] for s in range(NumShifts)])

# Constraints: Ensure that for each shift the required number of officers is on duty
for s in range(NumShifts):
    problem += (officers_starting[s] + officers_starting[(s + 1) % NumShifts] >= OfficersNeeded[s])

# Solve the problem
problem.solve()

# Gather the results
officers_assigned = [int(officers_starting[s].varValue) for s in range(NumShifts)]
total_cost = pulp.value(problem.objective)

# Output the results
output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(f'Result: {output} (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')