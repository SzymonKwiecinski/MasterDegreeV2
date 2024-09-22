import pulp
import json

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Problem Initialization
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("Police_Officer_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * (officers_assigned[s] + officers_assigned[s+1]) for s in range(S-1)) + \
                      pulp.lpSum(shift_costs[S-1] * officers_assigned[S-1]), "Total_Cost"

# Constraints
for s in range(S):
    if s < S - 1:
        problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"OfficersNeeded_{s}"

# Solve the problem
problem.solve()

# Output results
officers_assigned_result = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')