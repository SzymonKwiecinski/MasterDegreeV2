import pulp

# Parse the data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Initialize the problem
problem = pulp.LpProblem("Minimize_Cost_of_Officer_Shifts", pulp.LpMinimize)

# Decision variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective function
total_cost = pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(S)])
problem += total_cost

# Constraints
for s in range(S):
    problem += (
        officers_assigned[s] + 
        officers_assigned[(s + 1) % S] >= officers_needed[s], 
        f"cover_shift_{s}"
    )

# Solve the problem
problem.solve()

# Extract the results
officers_assigned_values = [int(officers_assigned[s].varValue) for s in range(S)]
total_cost_value = pulp.value(problem.objective)

# Output the results
result = {
    "officers_assigned": officers_assigned_values,
    "total_cost": total_cost_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')