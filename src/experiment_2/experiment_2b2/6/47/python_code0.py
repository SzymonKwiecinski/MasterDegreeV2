import pulp

# Read data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the Linear Programming problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(num_shifts)]

# Objective function: Minimize the total cost
problem += pulp.lpSum([x[i] * shift_costs[i] for i in range(num_shifts)])

# Constraints
for i in range(num_shifts):
    problem += x[i] + x[(i + 1) % num_shifts] >= officers_needed[i]

# Solve the problem
problem.solve()

# Prepare the output
officers_assigned = [int(x[i].varValue) for i in range(num_shifts)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')