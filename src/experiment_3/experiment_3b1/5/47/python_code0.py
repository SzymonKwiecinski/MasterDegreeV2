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
shift_cost = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Shift_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
officers_assigned = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Continuous') for s in range(1, S + 1)]
y = [pulp.LpVariable(f'y_{s}', cat='Binary') for s in range(1, S + 1)]

# Objective Function
problem += pulp.lpSum(shift_cost[s - 1] * y[s - 1] for s in range(1, S + 1)), "Total_Cost"

# Constraints
for s in range(1, S + 1):
    problem += officers_assigned[s - 1] >= officers_needed[s - 1], f"Officers_Needed_{s}"

# Recursive Constraints
for s in range(3, S + 1):
    problem += officers_assigned[s - 1] == officers_assigned[s - 2] + officers_assigned[s - 3], f"Recursive_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
for s in range(1, S + 1):
    print(f'Officers assigned to shift {s}: {officers_assigned[s - 1].varValue}')

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')