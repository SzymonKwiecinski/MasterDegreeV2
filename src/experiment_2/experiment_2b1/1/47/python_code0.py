import json
import pulp

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Extract necessary variables
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision Variables: Number of officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective Function: Minimize total cost
total_cost = pulp.lpSum(shift_costs[s] * (officers_assigned[s] + officers_assigned[s-1] if s > 0 else officers_assigned[s]) for s in range(S))
problem += total_cost

# Constraints: Ensure that the number of officers assigned meets the required officers needed for each shift
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s] - (officers_assigned[s-1] if s > 0 else 0), f"OfficersNeeded_Constraint_{s}"

# Solve the problem
problem.solve()

# Extract results
assigned_officers = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost_value = pulp.value(problem.objective)

# Prepare output
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost_value
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost_value}</OBJ>')