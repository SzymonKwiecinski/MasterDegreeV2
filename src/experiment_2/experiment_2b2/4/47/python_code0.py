import pulp

# Input data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}

num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Define the Linear Programming problem
problem = pulp.LpProblem("ShiftScheduling", pulp.LpMinimize)

# Decision variables: number of officers starting at shift s
officers_starting = pulp.LpVariable.dicts("OfficersStarting", range(num_shifts), lowBound=0, cat='Integer')

# Objective function: Minimize the total cost
problem += pulp.lpSum([shift_costs[s] * officers_starting[s] for s in range(num_shifts)])

# Constraints: The number of officers on duty for each shift must meet or exceed the required number
for s in range(num_shifts):
    problem += (
        officers_starting[s] + officers_starting[(s - 1) % num_shifts] >= officers_needed[s],
        f"ShiftCoverage{s}"
    )

# Solve the problem
problem.solve()

# Prepare output data
officers_assigned = [int(officers_starting[s].varValue) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)
output_data = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(f'Output: {output_data}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')