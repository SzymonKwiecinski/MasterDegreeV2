import pulp
import json

data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extracting needed data
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Officer_Shifts", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'Officers_Assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

# Constraints: Each shift must have enough officers
for s in range(num_shifts):
    if s < num_shifts - 1:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f'OfficersNeededForShift_{s}'

# Solve the problem
problem.solve()

# Collect the results
assigned_officers = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Output the results in the specified format
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')