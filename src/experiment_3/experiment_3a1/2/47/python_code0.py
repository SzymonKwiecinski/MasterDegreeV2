import pulp

# Data from the provided JSON format
data = {
    'NumShifts': 6,
    'OfficersNeeded': [15, 13, 11, 11, 9, 7],
    'ShiftCosts': [500, 480, 450, 460, 470, 490]
}

# Define the problem
problem = pulp.LpProblem("PoliceShiftAssignment", pulp.LpMinimize)

# Define decision variables
num_shifts = data['NumShifts']
officers_needed = data['OfficersNeeded']
shift_costs = data['ShiftCosts']

# Binary variable indicating if shift s is assigned
x = pulp.LpVariable.dicts("ShiftAssigned", range(1, num_shifts + 1), cat='Binary')

# Continuous variable for the number of officers assigned to each shift
officers_assigned = pulp.LpVariable.dicts("OfficersAssigned", range(1, num_shifts + 1), lowBound=0, cat='Continuous')

# Objective function: Minimize the total cost
problem += pulp.lpSum(shift_costs[s - 1] * x[s] for s in range(1, num_shifts + 1)), "TotalCost"

# Constraints
for s in range(1, num_shifts + 1):
    problem += officers_assigned[s] >= officers_needed[s - 1], f"OfficersNeeded_{s}"

for s in range(2, num_shifts + 1):
    problem += officers_assigned[s] <= officers_assigned[s - 1] + 2 * x[s], f"OfficerLimit_{s}"

problem += officers_assigned[1] <= 2 * x[1], "OfficerLimit_1"

# Solve the problem
problem.solve()

# Get the results
officers_assigned_values = [officers_assigned[s].varValue for s in range(1, num_shifts + 1)]
total_cost = pulp.value(problem.objective)

# Output the results
print(f"Officers Assigned: {officers_assigned_values}")
print(f'Total Cost: <OBJ>{total_cost}</OBJ>')