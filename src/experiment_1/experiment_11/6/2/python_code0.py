import pulp

# Data from the problem
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Create the linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable("N", lowBound=0, cat='Integer')

# Objective function
problem += N, "Total_Nurses_Hired"

# Constraints
for t in range(data['T']):
    problem += N >= data['Demand'][t], f"Demand_Constraint_day_{t + 1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')