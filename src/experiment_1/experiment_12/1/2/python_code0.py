import pulp

# Data
data = {
    'T': 7,
    'Period': 4,
    'Demand': [0, 5, 9, 15, 4, 7, 3]
}

# Initialize the problem
problem = pulp.LpProblem("Nurse_Staffing", pulp.LpMinimize)

# Decision Variables
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective Function
problem += N, "Minimize_the_number_of_nurses"

# Constraints
for t in range(data['T']):
    problem += N >= data['Demand'][t], f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')