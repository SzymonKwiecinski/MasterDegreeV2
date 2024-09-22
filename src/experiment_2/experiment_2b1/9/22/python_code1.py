import pulp
import json

data = {'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
        'strength': [2000, 1500, 1000], 
        'lessonewaste': [0.25, 0.2, 0.1], 
        'moreonewaste': [0.1, 0.05, 0.05], 
        'recruit': [500, 800, 500], 
        'costredundancy': [200, 500, 500], 
        'num_overman': 150, 
        'costoverman': [1500, 2000, 3000], 
        'num_shortwork': 50, 
        'costshort': [500, 400, 400]}

K = len(data['strength'])  # Number of manpower categories
I = len(data['requirement'][0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Define decision variables
recruit = pulp.LpVariable.dicts("Recruit", (range(K), range(I)), lowBound=0, upBound=500)
overmanning = pulp.LpVariable.dicts("Overmanning", (range(K), range(I)), lowBound=0, upBound=data['num_overman'])
short = pulp.LpVariable.dicts("Short", (range(K), range(I)), lowBound=0, upBound=data['num_shortwork'])

# Objective function: Minimize redundancy costs
cost_redundancy = pulp.lpSum(data['costredundancy'][k] * (
    data['strength'][k] + 
    pulp.lpSum(recruit[k][i] for i in range(I)) - 
    pulp.lpSum(overmanning[k][i] for i in range(I)) - 
    pulp.lpSum(short[k][i] for i in range(I))/2 - 
    pulp.lpSum(data['requirement'][k][j] for j in range(I)) 
) for k in range(K))

problem += cost_redundancy

# Constraints for each category of manpower for each year
for k in range(K):
    for i in range(I):
        problem += (pulp.lpSum(recruit[k][j] for j in range(i+1)) 
                     + data['strength'][k] 
                     - pulp.lpSum(overmanning[k][j] for j in range(I)) 
                     - pulp.lpSum(short[k][j] for j in range(I))/2 
                     >= data['requirement'][k][i], 
                     f"Manpower_Requirement_Constraint_k{k}_i{i}")

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "recruit": [[pulp.value(recruit[k][i]) for i in range(I)] for k in range(K)],
    "overmanning": [[pulp.value(overmanning[k][i]) for i in range(I)] for k in range(K)],
    "short": [[pulp.value(short[k][i]) for i in range(I)] for k in range(K)]
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')