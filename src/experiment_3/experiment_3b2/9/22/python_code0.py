import pulp
import json

# Data in JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Extract data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = len(strength)
I = len(requirement[0])

# Define the problem
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

# Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(costredundancy[k] * 
                      (strength[k] - requirement[k][i] + recruit[k][i] - short[k][i] * 0.5) 
                      for k in range(K) for i in range(I))

# Constraints
for i in range(I):
    for k in range(K):
        if i == 0:  # First year
            prev_strength = strength[k]
        else:  # Subsequent years
            prev_strength = (strength[k] - moreonewaste[k] * strength[k] + 
                             pulp.lpSum(recruit[k][j] for j in range(i)) - 
                             pulp.lpSum(short[k][j] * 0.5 for j in range(i)))
        
        # Manpower balance
        problem += (prev_strength - (moreonewaste[k] * prev_strength) + 
                     recruit[k][i] - (lessonewaste[k] * recruit[k][i]) + 
                     overmanning[k][i] - short[k][i] * 0.5 >= 0)
        
        # Meet manpower requirement
        problem += (prev_strength >= requirement[k][i] - 
                    overmanning[k][i] - short[k][i] * 0.5)
        
        # Recruitment limit
        problem += recruit[k][i] <= recruit_limit[k]
        
        # Overmanning limit
        problem += pulp.lpSum(overmanning[k][i] for k in range(K)) <= num_overman
        
        # Short-time limit
        problem += short[k][i] <= num_shortwork
        
# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')