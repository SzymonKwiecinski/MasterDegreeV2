import pulp

# Data from the provided JSON format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Define the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Continuous')

# Objective function
problem += N, "Minimize_Number_of_Nurses"

# Constraints
for t in range(data['T']):
    problem += N >= data['Demand'][t], f"Demand_Constraint_{t+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')