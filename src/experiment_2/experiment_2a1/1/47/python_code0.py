import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
S = data['NumShifts']

# Create the LP problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables: Number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([shift_costs[s] * (officers_assigned[s] + officers_assigned[s+1] if s < S-1 else officers_assigned[s]) for s in range(S)]), "Total Cost"

# Constraints: Ensure that the number of officers assigned meets the required officers needed
for s in range(S):
    if s < S - 1:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"OfficersNeededShift{s+1}"
    else:
        problem += officers_assigned[s] >= officers_needed[s], f"OfficersNeededShift{s+1}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "officers_assigned": [int(officers_assigned[s].varValue) for s in range(S)],
    "total_cost": pulp.value(problem.objective)
}

# Print output
print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')