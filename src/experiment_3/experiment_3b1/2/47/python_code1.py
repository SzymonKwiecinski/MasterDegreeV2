import pulp
import json

# Data
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem Definition
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision Variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(1, num_shifts + 1), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(shift_costs[s - 1] * pulp.ceil(officers_needed[s - 1] / 2) for s in range(1, num_shifts + 1))

# Constraints
problem += officers_assigned[1] >= officers_needed[0]  # First shift constraint
for s in range(2, num_shifts + 1):
    problem += officers_assigned[s] + officers_assigned[s - 1] >= officers_needed[s - 1]

# Last shift wrap-around constraint
problem += officers_assigned[num_shifts] + officers_assigned[num_shifts - 1] >= officers_needed[num_shifts - 1]

# Solve the problem
problem.solve()

# Output the results
officers_assigned_values = [officers_assigned[s].varValue for s in range(1, num_shifts + 1)]
total_cost = pulp.value(problem.objective)

print(f'Officers Assigned to each Shift: {officers_assigned_values}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')