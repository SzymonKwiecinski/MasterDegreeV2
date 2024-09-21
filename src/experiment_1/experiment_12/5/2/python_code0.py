import pulp

# Input data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Define the decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Define the objective function
problem += N, "Minimize number of nurses"

# Define the constraints
for t in range(T):
    problem += N >= demand[t], f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')