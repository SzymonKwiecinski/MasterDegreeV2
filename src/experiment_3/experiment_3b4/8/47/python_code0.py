import pulp

# Extract data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost_of_Shifts", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x{s}', lowBound=0, cat='Continuous') for s in range(num_shifts)]

# Objective function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(num_shifts))

# Constraints
for s in range(num_shifts):
    problem += x[s] + x[(s + 1) % num_shifts] >= officers_needed[s]

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')