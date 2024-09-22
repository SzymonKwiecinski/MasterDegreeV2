import pulp
import json

# Data input
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

K = range(len(data['strength']))  # Manpower categories
I = range(len(data['requirement'][0]))  # Planning years

# Create the problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

# Decision variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (K, I), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * (data['strength'][k] - data['requirement'][k][i] + recruit[k][i] + overmanning[k][i] + 0.5 * short[k][i])
    for k in K for i in I
), "Total_Redundancy_Cost"

# Constraints
for k in K:
    for i in I:
        # Strength update based on wastage and recruitment
        if i > 0:
            problem += (data['strength'][k] * (1 - data['moreonewaste'][k]) +
                        recruit[k][i-1] * (1 - data['lessonewaste'][k]) + 
                        recruit[k][i] >= data['requirement'][k][i]), f"Strength_Requirement_Category_{k}_Year_{i}"
        
        # Recruitment limits
        problem += recruit[k][i] <= data['recruit'][k], f"Recruitment_Limit_Category_{k}_Year_{i}"
        
        # Overmanning limits
        problem += overmanning[k][i] <= data['num_overman'], f"Overmanning_Limit_Category_{k}_Year_{i}"
        
        # Short-time work limits
        problem += short[k][i] <= data['num_shortwork'], f"Short_Time_Work_Limit_Category_{k}_Year_{i}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')