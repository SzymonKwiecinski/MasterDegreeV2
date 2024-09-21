import pulp

# Data from the JSON format
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')  # Number of nurses to hire

# Objective function
problem += N, "Minimize number of nurses"

# Constraints
for t in range(data['T']):
    demand_t = data['Demand'][t]
    problem += N >= demand_t, f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')