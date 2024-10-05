import pulp

# Data input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the LP problem
problem = pulp.LpProblem("Police_Shift_Allocation", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("Officers_Assigned", range(num_shifts), lowBound=0, cat=pulp.LpInteger)

# Objective function
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

# Constraints
for s in range(num_shifts):
    problem += (officers_assigned[s] + officers_assigned[(s+1) % num_shifts] >= officers_needed[s], f"Requirement_{s}")

# Solve the problem
problem.solve()

# Extract the results
officers_assigned_result = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Prepare the output
output = {
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')