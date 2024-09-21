import pulp

# Data from the JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extract the number of days and demand
T = data['T']
Demand = data['Demand']

# Define the optimization problem
problem = pulp.LpProblem("Nurse_Staffing", pulp.LpMinimize)

# Decision variable: N (number of nurses to hire)
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective function: Minimize N
problem += N, "Minimize the number of nurses"

# Constraints: N >= Demand_t for all t
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Print the result
print(f'N (Number of Nurses to Hire): {pulp.value(N)}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')