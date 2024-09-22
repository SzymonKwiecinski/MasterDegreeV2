import pulp

# Data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Linear Programming Problem
problem = pulp.LpProblem("Minimize_Officer_Assignment_Cost", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(S), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(S)), "Total_Cost"

# Constraints
for s in range(S):
    problem += x[s] + x[(s - 1) % S] >= officers_needed[s], f"Officers_Needed_{s+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')