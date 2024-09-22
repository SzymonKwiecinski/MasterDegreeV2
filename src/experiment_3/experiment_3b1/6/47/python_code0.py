import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Number of shifts
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Problem definition
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S - 1):
    problem += x[s] + x[s + 1] >= officers_needed[s], f"Officers_Needed_Constraint_{s+1}"

# Last shift constraint
problem += x[S - 1] >= officers_needed[S - 1], "Officers_Needed_Last_Shift"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')