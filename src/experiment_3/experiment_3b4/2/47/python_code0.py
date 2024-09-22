import pulp

# Define the problem
problem = pulp.LpProblem("Shift_Scheduling", pulp.LpMinimize)

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Decision variables
x = pulp.LpVariable.dicts('x', range(data['NumShifts']), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(data['ShiftCosts'][s] * x[s] for s in range(data['NumShifts'])), "Total Cost"

# Constraints
for s in range(data['NumShifts']):
    problem += (x[s] + (x[s-1] if s > 0 else 0) >= data['OfficersNeeded'][s]), f"Officers_Needed_Shift_{s}"

# Solve the problem
problem.solve()

# Print the solution
for v in problem.variables():
    print(f'{v.name} = {v.varValue}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')