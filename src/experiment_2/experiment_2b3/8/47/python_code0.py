import pulp

# Parse the data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables: number of officers starting at each shift
officers_assigned = [pulp.LpVariable(f"officers_starting_shift_{s}", lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([shift_costs[s] * officers_assigned[s] for s in range(num_shifts)])

# Constraints: Ensure enough officers are present in each shift
for s in range(num_shifts):
    first_shift = s
    second_shift = (s + 1) % num_shifts
    problem += officers_assigned[first_shift] + officers_assigned[second_shift] >= officers_needed[s]

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Collect the results
officers_assigned_result = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

# Print the results
print({
    "officers_assigned": officers_assigned_result,
    "total_cost": total_cost
})
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')