import pulp

# Data parsing
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Demand = data['Demand']

# Initialize the problem
problem = pulp.LpProblem("Nurse_Staffing", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective function
problem += N, "Minimize_Number_of_Nurses"

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_Day_{t+1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')