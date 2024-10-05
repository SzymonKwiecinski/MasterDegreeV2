import pulp

# Data from JSON
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables: number of officers starting at each shift
x = pulp.LpVariable.dicts("officers_starting_shift", range(S), lowBound=0, cat='Integer')

# Objective function: Minimize the total cost
problem += pulp.lpSum([shift_costs[s] * x[s] for s in range(S)])

# Constraints: Ensure the number of officers on duty for each shift
for s in range(S):
    problem += (x[s] + x[(s - 1) % S]) >= officers_needed[s]

# Solve the problem
problem.solve()

# Output results
officers_assigned = [pulp.value(x[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')