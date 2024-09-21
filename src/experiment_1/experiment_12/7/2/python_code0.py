import pulp

# Data from JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extracting the data
T = data['T']
demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective function
problem += N, "Number of Nurses to Hire"

# Constraints
for t in range(T):
    problem += N >= demand[t], f"Demand_Constraint_Day_{t+1}"

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')