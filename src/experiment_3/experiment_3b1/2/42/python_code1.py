import pulp

# Data from the provided JSON
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 
        'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Number of depots and ports
I = len(data['numdepot'])
J = len(data['numport'])

# Create the problem
problem = pulp.LpProblem("Container_Transport", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((number[i][j] * data['distance'][i][j] * data['price'] / 2)
                       for i in range(I) for j in range(J)), "Total_Transportation_Cost"

# Supply constraints at each depot
for i in range(I):
    problem += pulp.lpSum(number[i][j] for j in range(J)) <= data['numdepot'][i], f"Supply_Constraint_depot_{i}"

# Demand constraints at each port
for j in range(J):
    problem += pulp.lpSum(number[i][j] for i in range(I)) >= data['numport'][j], f"Demand_Constraint_port_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')