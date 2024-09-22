import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
num_shifts = data['NumShifts']

# Create the problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'Officers_Assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] // 2) for s in range(num_shifts)), "Total Cost"

# Constraints
for s in range(num_shifts):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Officers_needed_{s}"
    elif s == num_shifts - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Officers_needed_{s}"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Officers_needed_{s}"

# Solve the problem
problem.solve()

# Prepare output
assigned_officers = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Output the solution
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
num_shifts = data['NumShifts']

# Create the problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'Officers_Assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function
# Shift cost is incurred for every officer assigned for each shift
problem += pulp.lpSum(shift_costs[s] * officers_assigned[s] for s in range(num_shifts)), "Total Cost"

# Constraints to ensure enough officers are present
for s in range(num_shifts):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Officers_needed_{s}"
    elif s == num_shifts - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Officers_needed_{s}"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Officers_needed_{s}"

# Solve the problem
problem.solve()

# Prepare output
assigned_officers = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Output the solution
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')