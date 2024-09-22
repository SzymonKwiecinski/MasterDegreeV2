import pulp
import json

# Input data
data = json.loads("{'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}")

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective function
problem += pulp.lpSum([shift_costs[s] * pulp.ceil(officers_assigned[s] / 2) for s in range(S)])

# Constraints
for s in range(S):
    # Ensure sufficient officers are assigned for each shift
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s]
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s]
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned_results = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output results
result = {
    "officers_assigned": officers_assigned_results,
    "total_cost": total_cost
}

print(json.dumps(result))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')