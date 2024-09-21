import pulp

# Data from the provided JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Create a linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective function
problem += N, "Minimize_the_number_of_nurses"

# Constraints
for t in range(data['T']):
    problem += N >= data['Demand'][t], f"Demand_constraint_day_{t+1}"

# Solving the problem
problem.solve()

# Print the result
print(f'N (Number of nurses to hire): {pulp.value(N)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')