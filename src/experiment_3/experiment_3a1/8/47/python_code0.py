import pulp

# Data from the JSON input
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Parameters
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_cost = data['ShiftCosts']

# Create the linear programming problem
problem = pulp.LpProblem("Police_Officer_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(1, S+1), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(shift_cost[s-1] * ((officers_assigned[s] + officers_assigned[s+1]) // 2)
                                           for s in range(1, S)), "Total_Cost"

# Constraints
for s in range(1, S):
    problem += (officers_assigned[s] + officers_assigned[s+1] >= officers_needed[s-1]), f"Constraint_{s}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')