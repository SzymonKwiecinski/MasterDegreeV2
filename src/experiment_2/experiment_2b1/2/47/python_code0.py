import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extract data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Define decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([shift_costs[s] * (officers_assigned[s] if s < S else 0) for s in range(S)])

# Constraints
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s]
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s]
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s]

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned_values = [officers_assigned[s].varValue for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output the result
result = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

# Print the output
print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')