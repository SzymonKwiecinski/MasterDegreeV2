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

K = len(data['strength'])
I = len(data['requirement'][0])

# Create the LP problem
problem = pulp.LpProblem("Minimize_Redundancy", pulp.LpMinimize)

# Decision variables
recruit_vars = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (data['strength'][k] - 
           (data['requirement'][k][i] + overmanning_vars[k][i] - short_vars[k][i])) 
           for k in range(K) for i in range(I)), "Total_Redundancy_Cost"

# Constraints
for k in range(K):
    for i in range(I):
        problem += (data['strength'][k] + pulp.lpSum(recruit_vars[k][j] for j in range(i + 1)) -
                     pulp.lpSum(short_vars[k][j] for j in range(i + 1)) -
                     overmanning_vars[k][i] >= data['requirement'][k][i] - data['num_overman'],
                     f"Manpower_Requirement_Constraint_k{k}_i{i}")

        problem += (overmanning_vars[k][i] <= data['num_overman'],
                     f"Overmanning_Constraint_k{k}_i{i}")

        problem += (short_vars[k][i] <= data['num_shortwork'],
                     f"Short_Work_Constraint_k{k}_i{i}")

        problem += (recruit_vars[k][i] <= data['recruit'][k],
                     f"Recruitment_Constraint_k{k}_i{i}")
        
# Solve the problem
problem.solve()

# Extract results
recruit_result = [[[int(recruit_vars[k][i].varValue) for i in range(I)] for k in range(K)]]
overmanning_result = [[[int(overmanning_vars[k][i].varValue) for i in range(I)] for k in range(K)]]
short_result = [[[int(short_vars[k][i].varValue) for i in range(I)] for k in range(K)]]

# Output results
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')