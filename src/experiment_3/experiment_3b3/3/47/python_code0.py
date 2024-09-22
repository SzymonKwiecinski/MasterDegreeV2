import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{s}', lowBound=0, cat='Continuous') for s in range(S)]
y = [pulp.LpVariable(f'y_{s}', cat='Binary') for s in range(S)]

# Objective Function
problem += pulp.lpSum(shift_costs[s] * y[s] for s in range(S))

# Constraints
for s in range(S):
    problem += x[s] >= officers_needed[s] * y[s], f"OfficerRequirement_shift_{s}"

for s in range(S - 1):
    problem += x[s] == x[s + 1], f"ConsecutiveShifts_{s}"

# Solve the problem
problem.solve()

# Output results
officers_assigned = [pulp.value(x[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f'Officers assigned to each shift: {officers_assigned}')
print(f'Total cost incurred: {total_cost}')
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')