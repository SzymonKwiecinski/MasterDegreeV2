import pulp

# Data
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("Officers_Start_Shift", (s for s in range(S)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(shift_cost[s] * x[s] for s in range(S))

# Constraints
for s in range(S):
    problem += x[s] + x[(s-1) % S] >= officers_needed[s], f"Shift_{s+1}_Coverage"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')