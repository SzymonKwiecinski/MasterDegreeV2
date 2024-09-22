import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
S = data['NumShifts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables: number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Integer')

# Objective function: minimize total cost
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] + officers_assigned[s + 1] if s < S - 1 else officers_assigned[s])
                      for s in range(S)), "Total Cost"

# Constraints: ensure the number of officers assigned meets the required numbers for each shift
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s], f"MinOfficersForShift{s}"
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"MinOfficersForShift{s}"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"MinOfficersForShift{s}"

# Solve the problem
problem.solve()

# Results
officers_assigned_values = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

# Print the results
print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')