import pulp

# Parse the problem data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

# Decision variables: Number of officers starting at each shift
officers_assigned = [pulp.LpVariable(f'OfficersShift_{i}', lowBound=0, cat='Integer') for i in range(num_shifts)]

# Objective function: Minimize total cost
problem += pulp.lpSum([shift_costs[i] * officers_assigned[i] for i in range(num_shifts)])

# Constraints: Meet officers needed for each shift with officers starting their shifts
for i in range(num_shifts):
    problem += (officers_assigned[i % num_shifts] + officers_assigned[(i + num_shifts - 1) % num_shifts] >= officers_needed[i])

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "officers_assigned": [int(pulp.value(officers_assigned[i])) for i in range(num_shifts)],
    "total_cost": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')