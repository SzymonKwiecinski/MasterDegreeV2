import pulp

# Extract data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

S = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the Linear Programming problem
problem = pulp.LpProblem("Police_Shift_Allocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("OfficersAssigned", range(S), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum([shift_costs[s] * x[s] for s in range(S)])

# Constraints
for s in range(S):
    if s == S - 1:
        problem += x[s] + x[0] >= officers_needed[s]
    else:
        problem += x[s] + x[s + 1] >= officers_needed[s]

# Solve the problem
problem.solve()

# Extract the results
officers_assigned = [x[s].varValue for s in range(S)]
total_cost = pulp.value(problem.objective)

# Output
output = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')