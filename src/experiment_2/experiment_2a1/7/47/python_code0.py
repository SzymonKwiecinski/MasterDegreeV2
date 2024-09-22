import pulp
import json

data = json.loads("{'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}")

S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("PoliceShiftAssignment", pulp.LpMinimize)

# Variables: Number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(S)]), "TotalCost"

# Constraints: Each shift must have enough officers
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s], f"MinOfficersNeeded_{s}"
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"MinOfficersNeeded_{s}"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"MinOfficersNeeded_{s}"

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned_list = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_list,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')