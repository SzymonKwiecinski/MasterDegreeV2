import pulp
import json

# Data in JSON format
data = '{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}'
data = json.loads(data)

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Continuous') for s in range(1, S + 1)]
shift_indicator = [pulp.LpVariable(f'x_{s}', cat='Binary') for s in range(1, S + 1)]

# Objective function
problem += pulp.lpSum(shift_costs[s - 1] * shift_indicator[s - 1] for s in range(1, S + 1)), "Total_Cost"

# Constraints
for s in range(1, S + 1):
    problem += officers_assigned[s - 1] >= officers_needed[s - 1], f"Officers_Assignment_Constraint_{s}"

for s in range(2, S + 1):
    problem += officers_assigned[s - 1] == officers_assigned[s - 2], f"Shift_Coverage_Constraint_{s}"

# Solve the problem
problem.solve()

# Output results
officers_assigned_result = [pulp.value(officers_assigned[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f'Officers Assigned: {officers_assigned_result}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')