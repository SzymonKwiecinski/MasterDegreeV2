import pulp

# Data from the JSON-like format
data = {'T': 7, 'Period': 4, 'Demand': [0, 5, 9, 15, 4, 7, 3]}
T = data['T']
Demand = data['Demand']

# Create the linear programming problem
problem = pulp.LpProblem("Nurse_Staffing_Problem", pulp.LpMinimize)

# Decision variable: Number of nurses to hire
N = pulp.LpVariable("N", lowBound=0, cat='Continuous')

# Objective function: Minimize the number of nurses
problem += N, "Total_Nurses_Hired"

# Constraints: Number of nurses must meet or exceed demand for each day
for t in range(T):
    problem += N >= Demand[t], f"Demand_Constraint_{t+1}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')