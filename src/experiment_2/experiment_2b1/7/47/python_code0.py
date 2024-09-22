import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Number of shifts and data extraction
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables: number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum([officers_assigned[s] * shift_costs[s] for s in range(S)]), "Total_Cost"

# Constraints: Ensure enough officers are assigned for each shift
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] >= officers_needed[s]
    elif s == S-1:
        problem += officers_assigned[s-1] + officers_assigned[s] >= officers_needed[s]
    else:
        problem += officers_assigned[s-1] + officers_assigned[s] >= officers_needed[s]

# Solve the problem
problem.solve()

# Gather results
officers_assigned_values = [pulp.value(officers_assigned[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output results
result = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')