import pulp

# Data from the JSON input
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extracting data
T = data['T']
Demand = data['Demand']

# Define the problem
problem = pulp.LpProblem("Nurse_Staffing", pulp.LpMinimize)

# Decision Variables
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective Function
problem += N

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')