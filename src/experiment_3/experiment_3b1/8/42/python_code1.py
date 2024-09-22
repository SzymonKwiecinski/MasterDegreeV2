import pulp
import json

# Load data from the provided JSON format
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')

# Extract data for ease of use
numdepots = len(data['numdepot'])
numports = len(data['numport'])
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Create the LP problem
problem = pulp.LpProblem("Transportation_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(numdepots), range(numports)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i][j] * distance[i][j] * price / 2) for i in range(numdepots) for j in range(numports)), "Total_Cost"

# Supply Constraints
for i in range(numdepots):
    problem += pulp.lpSum(x[i][j] for j in range(numports)) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand Constraints
for j in range(numports):
    problem += pulp.lpSum(x[i][j] for i in range(numdepots)) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')