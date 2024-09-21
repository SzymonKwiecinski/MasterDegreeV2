import pulp

# Data from the JSON
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}

# Extracting data
T = data['T']
Demand = data['Demand']

# Create a Linear Programming Minimization Problem
problem = pulp.LpProblem("Nurse_Staffing", pulp.LpMinimize)

# Decision Variables
# Number of nurses to hire
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective Function
# Minimize the number of nurses
problem += N, "Objective"

# Constraints
# Ensuring the number of nurses meets or exceeds the demand for each day
for t in range(T):
    problem += N >= Demand[t], f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')