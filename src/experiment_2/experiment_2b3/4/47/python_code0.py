import pulp

# Parse the data
data = {'NumShifts': 6, 'OfficersNeeded': [15, 13, 11, 11, 9, 7], 'ShiftCosts': [500, 480, 450, 460, 470, 490]}
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Initialize the problem
problem = pulp.LpProblem("Minimize_Shift_Cost", pulp.LpMinimize)

# Define decision variables: number of officers starting their shift at each shift
x = [pulp.LpVariable(f'x{s}', lowBound=0, cat='Integer') for s in range(num_shifts)]

# Objective function: Minimize total cost
problem += pulp.lpSum(shift_costs[s] * x[s] for s in range(num_shifts)), "Total_Cost"

# Constraints: Ensure enough officers are on duty for each shift
for s in range(num_shifts):
    problem += x[s] + x[(s + 1) % num_shifts] >= officers_needed[s], f"Shift_Coverage_{s}"

# Solve the problem
problem.solve()

# Collect the results
officers_assigned = [pulp.value(x[s]) for s in range(num_shifts)]
total_cost = pulp.value(problem.objective)

solution = {
    "officers_assigned": officers_assigned,
    "total_cost": total_cost
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')