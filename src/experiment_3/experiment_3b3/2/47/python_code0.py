import pulp

# Data from provided JSON
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Problem variables
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create a linear programming problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables
assigned_officers = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Continuous') for s in range(num_shifts)]

# Objective function
problem += pulp.lpSum([shift_costs[s] * assigned_officers[s] for s in range(num_shifts)])

# Constraints
for s in range(num_shifts - 1):
    problem += assigned_officers[s] + assigned_officers[s + 1] >= officers_needed[s]

problem += assigned_officers[num_shifts - 1] >= officers_needed[num_shifts - 1]

# Solve the problem
problem.solve()

# Print results
assigned_values = [pulp.value(assigned_officers[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

print(f'Assigned Officers per Shift: {assigned_values}')
print(f'Total Cost: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')