import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create a linear programming problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: minimize total cost
total_cost = pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])
problem += total_cost

# Constraints: each shift's officers assigned needs to meet or exceed those needed
for s in range(num_shifts):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s]   # First shift
    else:
        problem += officers_assigned[s] + officers_assigned[s - 1] >= officers_needed[s]  # Subsequent shifts

# Solve the problem
problem.solve()

# Prepare output
officers_assigned_values = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost_value = pulp.value(problem.objective)

# Output data
output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost_value
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')