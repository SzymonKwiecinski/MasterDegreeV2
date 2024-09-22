import pulp
import json

data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extracting values from the data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables: the number of officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'Officers_Assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective Function: Minimize total cost
problem += pulp.lpSum([shift_costs[s] for s in range(S)])  # Total cost (not directly dependent on assignments)

# Constraints: Ensure officers assigned can cover the needed officers
for s in range(S):
    if s == 0:  # First shift
        problem += officers_assigned[s] >= officers_needed[s], f"Officer_Need_Constraint_{s}"
    else:  # For all other shifts, consider the previous shift
        problem += officers_assigned[s-1] + officers_assigned[s] >= officers_needed[s], f"Officer_Need_Constraint_{s}"

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned_values = [int(officers_assigned[s].value()) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output the result
output = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

# Printing the objective value as required
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')