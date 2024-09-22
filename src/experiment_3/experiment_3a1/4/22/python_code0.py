import pulp
import json

# Load data from JSON format
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

# Model setup
problem = pulp.LpProblem("Minimize_Redundancy_Cost", pulp.LpMinimize)

K = len(data['strength'])  # Number of categories
I = len(data['requirement'])  # Number of years

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(K), range(I)), lowBound=0, cat='Continuous')  # recruits
y = pulp.LpVariable.dicts("y", (range(K), range(I)), lowBound=0, cat='Continuous')  # overmanning workers
z = pulp.LpVariable.dicts("z", (range(K), range(I)), lowBound=0, cat='Continuous')  # short-time workers

# Objective Function
problem += pulp.lpSum(data['costredundancy'][k] * 
                       pulp.lpSum(pulp.max(0, data['strength'][k] + x[k][i] - z[k][i] - y[k][i] - data['requirement'][i][k]) 
                                  for i in range(I)) 
                       for k in range(K)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        # Manpower requirement constraint
        problem += (data['strength'][k] + x[k][i] - z[k][i] - y[k][i] >= data['requirement'][i][k], 
                     f"ManpowerRequirement_k{k}_i{i}")
        
        # Recruitment constraint
        problem += (x[k][i] <= data['recruit'][k], f"Recruitment_k{k}_i{i}")
        
        # Overmanning constraint
        problem += (y[k][i] <= data['num_overman'], f"Overmanning_k{k}_i{i}")
        
        # Short-time working constraint
        problem += (z[k][i] <= data['num_shortwork'], f"ShortTimeWork_k{k}_i{i}")

# Non-negativity constraints are already implied by the lowBound=0 in variable declaration

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')