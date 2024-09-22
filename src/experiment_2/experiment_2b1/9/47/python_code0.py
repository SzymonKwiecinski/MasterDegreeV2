import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
num_shifts = data['NumShifts']

# Create the LP problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(num_shifts), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([shift_costs[s] * (officers_assigned[s] + officers_assigned[s+1]) for s in range(num_shifts-1)]) + \
                 pulp.lpSum([shift_costs[num_shifts-1] * officers_assigned[num_shifts-1]]), "Total_Cost"

# Constraints
for s in range(num_shifts):
    if s < num_shifts - 1:
        problem += officers_assigned[s] + officers_assigned[s+1] >= officers_needed[s], f"Need_Officers_Shift_{s+1}"
    else:
        problem += officers_assigned[s] >= officers_needed[s], f"Need_Officers_Shift_{s+1}"

# Solve the problem
problem.solve()

# Output results
officers_assigned_values = [int(officers_assigned[s].value()) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')