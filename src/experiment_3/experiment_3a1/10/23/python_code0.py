import pulp
import json

# Load data from JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extract data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strength)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Create the Linear Programming problem
problem = pulp.LpProblem("Manpower_Requirements_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("recruits", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
y = pulp.LpVariable.dicts("overman", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')
z = pulp.LpVariable.dicts("shorttime", ((k, i) for k in range(K) for i in range(I)), lowBound=0, upBound=None, cat='Integer')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * (strength[k] - requirement[k][i]) + 
                      costoverman[k] * y[k, i] + 
                      costshort[k] * z[k, i] 
                      for k in range(K) for i in range(I))

# Constraints
for k in range(K):
    for i in range(I):
        problem += (strength[k] - 
                     lessonewaste[k] * x[k, i] - 
                     moreonewaste[k] * (strength[k] - x[k, i]) + 
                     y[k, i] + 
                     z[k, i] / 2 >= requirement[k][i])

# Recruitment capacity constraint
for i in range(I):
    problem += pulp.lpSum(x[k, i] for k in range(K)) <= pulp.lpSum(recruit[k] for k in range(K))

# Overman constraint
for i in range(I):
    problem += pulp.lpSum(y[k, i] for k in range(K)) <= num_overman

# Short-time worker constraint
for i in range(I):
    problem += pulp.lpSum(z[k, i] for k in range(K)) <= num_shortwork

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')