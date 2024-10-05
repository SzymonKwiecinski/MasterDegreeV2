import pulp

# Parse data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the problem
problem = pulp.LpProblem("Police_Scheduling_Problem", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f'officers_assigned_{s}', lowBound=0, cat='Integer') for s in range(S)]

# Objective Function
problem += pulp.lpSum([shift_costs[s] * x[s] for s in range(S)])

# Constraints
for s in range(S):
    problem += x[s] + x[(s+1) % S] >= officers_needed[s]

# Solve the problem
problem.solve()

# Extract the results
officers_assigned = [pulp.value(x[s]) for s in range(S)]
total_cost = pulp.value(problem.objective)

output_data = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output_data)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')