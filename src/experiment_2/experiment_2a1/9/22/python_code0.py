import pulp
import json

# Input data
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    'strength': [2000, 1500, 1000], 
    'lessonewaste': [0.25, 0.2, 0.1], 
    'moreonewaste': [0.1, 0.05, 0.05], 
    'recruit': [500, 800, 500], 
    'costredundancy': [200, 500, 500], 
    'num_overman': 150, 
    'costoverman': [1500, 2000, 3000], 
    'num_shortwork': 50, 
    'costshort': [500, 400, 400]
}

# Problem parameters
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
cost_redundancy = data['costredundancy']
num_overman = data['num_overman']
cost_overman = data['costoverman']
num_shortwork = data['num_shortwork']
cost_short = data['costshort']

K = len(strength)  # Number of manpower categories
I = len(requirement[0])  # Number of years

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Integer')

# Objective function: minimize total redundancy cost
problem += pulp.lpSum(cost_redundancy[k] * overmanning[k, i] for k in range(K) for i in range(I)), "Total_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        # Total worker balance in each year
        problem += (strength[k] - (pulp.lpSum(recruit[k, j] for j in range(i + 1)) +
                                     pulp.lpSum(short[k, j] for j in range(i + 1)) -
                                     pulp.lpSum(overmanning[k, j] for j in range(i + 1)) * 0.5) <=
                     requirement[k][i] + num_overman), f"Balance_Constraint_k{k}_i{i}")

        # Recruit limits
        problem += (recruit[k, i] <= recruit_limit[k]), f"Recruit_Limit_k{k}_i{i}"

        # Short-time work limits
        problem += (short[k, i] <= num_shortwork), f"Short_Time_Limit_k{k}_i{i}"

        # Overmanning limits
        problem += (overmanning[k, i] <= (strength[k] + num_overman)), f"Overmanning_Limit_k{k}_i{i}"

# Solve the problem
problem.solve()

# Prepare output
output_recruit = [[[int(recruit[k, i].varValue) for i in range(I)] for k in range(K)]]
output_overmanning = [[[int(overmanning[k, i].varValue) for i in range(I)] for k in range(K)]]
output_short = [[[int(short[k, i].varValue) for i in range(I)] for k in range(K)]]

output = {
    "recruit": output_recruit,
    "overmanning": output_overmanning,
    "short": output_short
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')