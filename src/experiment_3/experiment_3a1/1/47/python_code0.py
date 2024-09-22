import pulp

# Data from the provided JSON format
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Number of shifts
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Create the problem
problem = pulp.LpProblem("Police_Shift_Assignment", pulp.LpMinimize)

# Decision variables
officers_assigned = pulp.LpVariable.dicts("officers_assigned", range(S), lowBound=0, cat='Continuous')
y = pulp.LpVariable.dicts("y", range(S), cat='Binary')

# Objective function
problem += pulp.lpSum(shift_costs[s] * y[s] for s in range(S)), "Total Cost"

# Constraints
# Officers assigned must meet or exceed needs
for s in range(S):
    problem += officers_assigned[s] >= officers_needed[s], f"Need_Constraint_{s}"

# Non-staffed shifts condition
for s in range(S):
    problem += officers_assigned[s] <= 10000 * y[s], f"Non_Staffed_Constraint_{s}"

# Consecutive shifts need to meet staffing requirements
for s in range(S - 1):
    problem += officers_assigned[s] + officers_assigned[s + 1] >= officers_needed[s], f"Consecutive_Needs_Constraint_{s}"

# Solve the problem
problem.solve()

# Output the results
officers_assigned_solution = [officers_assigned[s].varValue for s in range(S)]
total_cost = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
print(f'Officers Assigned: {officers_assigned_solution}')