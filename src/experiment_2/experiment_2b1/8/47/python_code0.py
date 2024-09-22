import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extracting parameters from the data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem variable
problem = pulp.LpProblem("Police_Shift_Optimization", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] + officers_assigned[s + 1] if s < S - 1 else officers_assigned[s]) for s in range(S)), "Total Cost"

# Constraints
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Shift_{s}_Constraint"
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Shift_{s}_Constraint"
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s], f"Shift_{s}_Constraint"

# Solve the problem
problem.solve()

# Prepare output
officers_assigned_values = [int(officers_assigned[s].value()) for s in range(S)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

# Print result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')