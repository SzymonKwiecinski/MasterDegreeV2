import pulp

# Parse the input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the LP problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables: number of officers assigned to each shift
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: minimize total cost
problem += pulp.lpSum([officers_assigned[s] * shift_costs[s] for s in range(num_shifts)])

# Constraints: meet the required number of officers for each shift
for s in range(num_shifts):
    problem += officers_assigned[s] + officers_assigned[(s + 1) % num_shifts] >= officers_needed[s]

# Solve the problem
problem.solve()

# Prepare the output
officers_solution = [int(officers_assigned[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_solution,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')