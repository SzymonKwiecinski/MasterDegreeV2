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

# Create the Linear Programming problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0)

# Objective Function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S):
    if s == 0:
        problem += x[s] >= officers_needed[s], f"Officers_Needed_Constraint_{s}"
    else:
        problem += x[s] + x[s - 1] >= officers_needed[s], f"Officers_Needed_Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')