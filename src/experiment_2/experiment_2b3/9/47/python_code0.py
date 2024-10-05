import pulp

# Extracting data from JSON input
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Initialize the Linear Programming problem
problem = pulp.LpProblem("Minimize_Police_Shift_Costs", pulp.LpMinimize)

# Define a list of decision variables
officers_assigned = [pulp.LpVariable(f'officers_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize total shift costs
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

# Constraints: Each shift's officer needs must be met
for s in range(num_shifts):
    problem += (officers_assigned[s] + officers_assigned[(s+1) % num_shifts] >= officers_needed[s])

# Solve the problem
problem.solve()

# Retrieve results
assigned_officers = [pulp.value(officers_assigned[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Output results
output = {
    "officers_assigned": assigned_officers,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')