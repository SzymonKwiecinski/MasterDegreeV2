import pulp
import json

# Input data
data = json.loads("{'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}")
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("PoliceShiftAssignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] // 2) for s in range(num_shifts)), "TotalCost"

# Constraints
for s in range(num_shifts):
    if s > 0:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"OfficersNeeded_{s}"
    else:
        problem += officers_assigned[s] >= officers_needed[s], f"OfficersNeeded_{s}"

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned_values = [int(var.value()) for var in officers_assigned]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')