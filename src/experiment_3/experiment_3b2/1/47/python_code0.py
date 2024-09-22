import pulp

# Data from the provided JSON format
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Number of shifts
S = data['NumShifts']

# Creating the Linear Programming problem
problem = pulp.LpProblem("Minimize_Shift_Costs", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['ShiftCosts'][s] * x[s] for s in range(S))

# Constraints
for s in range(S):
    if s == 0:
        problem += x[s] >= data['OfficersNeeded'][s]
    else:
        problem += x[s] + x[s-1] >= data['OfficersNeeded'][s]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')