import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

# Problem setup
A = len(data['young_clicks'])
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

# Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=data['max_clicks'], cat='Continuous')

# Objective Function: Maximize total unique clicks
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

# Constraints
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget'], "Budget_Constraint"
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Constraint"

# Solve the problem
problem.solve()

# Results
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')