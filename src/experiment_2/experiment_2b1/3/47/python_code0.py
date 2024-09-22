import pulp
import json

# Input data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Officers_Assignment", pulp.LpMinimize)

# Define variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize total cost
problem += pulp.lpSum(shift_costs[s] * officers_assigned[s] for s in range(num_shifts)), "Total_Cost"

# Constraints: Each shift must meet the officers needed
for s in range(num_shifts):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Officers_Needed_Shift_{s}"
    elif s == num_shifts - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Officers_Needed_Shift_{s}"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Officers_Needed_Shift_{s}"

# Solve the problem
problem.solve()

# Gather the results
officers_assigned_result = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Prepare output
output = {
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
}

# Print the output and the objective value
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')