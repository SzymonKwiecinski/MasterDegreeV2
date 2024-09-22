import pulp
import json

# Load data from JSON format
data = json.loads('{"NumShifts": 6, "OfficersNeeded": [15, 13, 11, 11, 9, 7], "ShiftCosts": [500, 480, 450, 460, 470, 490]}')

# Extract parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables: Number of officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(1, S + 1)]

# Objective function: Minimize total cost
problem += pulp.lpSum(shift_cost[s-1] * officers_assigned[s-1] for s in range(1, S + 1)), "Total_Cost"

# Constraints
# Constraint for the first shift
problem += officers_assigned[0] >= officers_needed[0], "First_Shift_Needed"

# Constraints for subsequent shifts
for s in range(2, S + 1):
    problem += (officers_assigned[s-1] + officers_assigned[s-2] >= officers_needed[s-1]), f"Shift_{s}_Needed"

# Solve the problem
problem.solve()

# Output the results
officers_assigned_values = [officers_assigned[s].varValue for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f'Assigned Officers: {officers_assigned_values}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')