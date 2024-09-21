import pulp

# Create the problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Data
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Demand = data['Demand']

# Decision Variable
N = pulp.LpVariable('N', lowBound=0, cat='Integer')

# Objective Function
problem += N, "Minimize number of nurses"

# Constraints
for t in range(T):
    problem += N >= Demand[t], f"Demand_constraint_day_{t+1}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')