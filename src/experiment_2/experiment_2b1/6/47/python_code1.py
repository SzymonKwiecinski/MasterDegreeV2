import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
num_shifts = data['NumShifts']

# Create a LP problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables: number of officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: minimize total cost
total_cost = pulp.lpSum(shift_costs[s] * (officers_assigned[s] // 2) for s in range(num_shifts))
problem += total_cost

# Constraints: satisfy officer needs for each shift
for s in range(num_shifts):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s]
    elif s == num_shifts - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s]
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "officers_assigned": [int(officers_assigned[s].varValue) for s in range(num_shifts)],
    "total_cost": pulp.value(problem.objective)
}

# Print the results
print(json.dumps(output))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')