import pulp

# Data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(num_shifts))

# Constraints
for s in range(num_shifts):
    problem += x[s] + x[s - 1] >= officers_needed[s]

# Solve
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')