import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Number of shifts
S = data['NumShifts']

# Officers needed per shift
officers_needed = data['OfficersNeeded']

# Shift costs
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Create decision variables for officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective function: minimize total cost
problem += pulp.lpSum([shift_costs[s] * (officers_assigned[s] // 2) for s in range(S)]), "Total Cost"

# Constraints: Ensure that the number of officers assigned meets the needs for each shift
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Shift_{s}_Officers_Needed"
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Shift_{s}_Officers_Needed"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Shift_{s}_Officers_Needed"

# Solve the problem
problem.solve()

# Collecting results
assigned_officers = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')