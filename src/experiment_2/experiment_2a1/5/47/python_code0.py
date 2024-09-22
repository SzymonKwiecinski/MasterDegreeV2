import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
S = data['NumShifts']

# Create the LP problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Define decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(S)])

# Constraints: Each shift must satisfy the officer requirement
for s in range(S):
    if s > 0:
        problem += officers_assigned[s] + officers_assigned[s-1] >= officers_needed[s], f"OfficerRequirement_shift_{s}"
    else:
        problem += officers_assigned[s] >= officers_needed[s], f"OfficerRequirement_shift_{s}"

# Solve the problem
problem.solve()

# Prepare output
result = {
    "officers_assigned": [int(officers_assigned[s].varValue) for s in range(S)],
    "total_cost": pulp.value(problem.objective)
}

# Print results
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')