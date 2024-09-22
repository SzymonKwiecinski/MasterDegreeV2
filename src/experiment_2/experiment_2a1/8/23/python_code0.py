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

# Define parameters from data
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

K = len(requirement)  # number of manpower types
I = len(requirement[0])  # number of years

# Create the LP problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
recruit_vars = pulp.LpVariable.dicts("Recruit", [(k, i) for k in range(K) for i in range(I)], lowBound=0, upBound=[recruit[k] for k in range(K)], cat='Integer')
overmanning_vars = pulp.LpVariable.dicts("Overmanning", [(k, i) for k in range(K) for i in range(I)], lowBound=0, cat='Integer')
short_vars = pulp.LpVariable.dicts("Short", [(k, i) for k in range(K) for i in range(I)], lowBound=0, upBound=num_shortwork, cat='Integer')

# Objective Function
total_cost = pulp.lpSum(recruit_vars[k, i] * 0 for k in range(K) for i in range(I)) + \
             pulp.lpSum(overmanning_vars[k, i] * costoverman[k] for k in range(K) for i in range(I)) + \
             pulp.lpSum(short_vars[k, i] * costshort[k] for k in range(K) for i in range(I))
problem += total_cost

# Constraints
for i in range(I):
    for k in range(K):
        # Wastage Calculation
        current_strength = strength[k] - (strength[k] * lessonewaste[k] + strength[k] * moreonewaste[k])
        
        # Ensure the workforce meets the requirements
        problem += current_strength + pulp.lpSum(recruit_vars[k, j] for j in range(i + 1)) + overmanning_vars[k, i] * num_overman >= requirement[k][i], f"Workforce_Requirement_{k}_{i}"

# Solve the problem
problem.solve()

# Collect results
recruit_result = [[[pulp.value(recruit_vars[k, i]) for i in range(I)] for k in range(K)]]
overmanning_result = [[[pulp.value(overmanning_vars[k, i]) for i in range(I)] for k in range(K)]]
short_result = [[[pulp.value(short_vars[k, i]) for i in range(I)] for k in range(K)]]

# Output results
output = {
    "recruit": recruit_result,
    "overmanning": overmanning_result,
    "short": short_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')