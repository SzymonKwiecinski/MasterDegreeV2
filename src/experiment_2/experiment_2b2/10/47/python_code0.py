import pulp

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

# Unpack the input data
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Initialize the problem
problem = pulp.LpProblem("Police_Shift_Scheduling", pulp.LpMinimize)

# Decision variables: Number of officers starting at shift s
x = [pulp.LpVariable(f"x{s}", lowBound=0, cat='Integer') for s in range(S)]

# Objective: Minimize total cost
problem += pulp.lpSum([shift_costs[s] * x[s] for s in range(S)])

# Constraints: Satisfy the officers needed for each shift
for s in range(S):
    problem += x[s] + x[(s-1) % S] >= officers_needed[s], f"OfficersNeeded_Shift{s}"

# Solve the problem
problem.solve()

# Extract the results
officers_assigned = [pulp.value(x[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output the results in the desired format
output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')