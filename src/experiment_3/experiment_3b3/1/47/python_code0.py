import pulp

# Data provided
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Number of shifts
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create a minimization problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Create decision variables for the number of officers assigned to each shift
x = pulp.LpVariable.dicts("Officers_Assigned", range(1, S + 1), lowBound=0, cat='Integer')

# Objective function: Minimize total cost
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, S + 1))

# Constraints

# Officers assignment for the first shift must satisfy the requirement
problem += x[1] >= officers_needed[0]

# For shifts 2 to S, ensure the requirement using two consecutive shifts
for s in range(2, S + 1):
    problem += x[s - 1] + x[s] >= officers_needed[s - 1]

# Solve the problem
problem.solve()

# Output the results
officers_assigned = [pulp.value(x[s]) for s in range(1, S + 1)]
total_cost = pulp.value(problem.objective)

print("Officers assigned to each shift:", officers_assigned)
print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')