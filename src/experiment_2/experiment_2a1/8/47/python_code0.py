import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']
S = data['NumShifts']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables: Number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Integer')

# Objective Function: Minimize the total cost
problem += pulp.lpSum(shift_costs[s] * pulp.ceil(officers_assigned[s] / 2) for s in range(S))

# Constraints: Each shift must have enough officers
for s in range(S):
    if s == 0:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s]
    elif s == S - 1:
        problem += officers_assigned[s - 1] + officers_assigned[s] >= officers_needed[s]
    else:
        problem += officers_assigned[s - 1] + officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Collect results
assigned_officers = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output the results
result = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

# Print final objective value
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')