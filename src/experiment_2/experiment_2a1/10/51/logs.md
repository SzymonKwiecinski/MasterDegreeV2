# START: OnePrompt 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Python. Based on description you solve given problem using Pulp python library. Python code place between ```python and ```. You receive the data in json format between: <DATA></DATA>. Do not change data format! Do not use `while` loop in python code! Do not include 'pip install' in script. Assume every python package is installed Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')`  
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO:

- Custom Tees is planning an online advertising campaign with \var{A} different ad types across two web companies.
- The company has set a goal of \var{goal_young} thousand clicks from visitors aged 18-25 and \var{goal_old} thousand clicks from visitors older than 25.
- The company has set a goal of \var{goal_unique_young} thousand unique clicks from visitors aged 18-25 and \var{goal_unique_old} thousand unique clicks from visitors older than 25.
- Ad type \var{a} has an estimated percentage of \var{young_click_{a}} clicks from the 18-25 age range.
- Ad type \var{a} has an estimated percentage of \var{old_click_{a}} clicks from older visitors.
- Ad type \var{a} has a cost of \var{cost_{a}} per 1000 clicks.
- Ad type \var{a} has a maximum allowable clicks of \var{max_click_{a}} in thousands.
- The estimated percentage of unique visitors for each ad type \var{a} is \var{unique_click_{a}}.
- The company has an advertising budget of $\var{budget}

INPUT FORMAT: 

{
    "goal_young": goal_young,
    "goal_old": goal_old,
    "goal_unique_young": goal_unique_young,
    "goal_unique_old": goal_unique_old,
    "young_clicks": [young_click_{a} for a in 1,...,A],
    "old_clicks": [old_click_{a} for a in 1,...,A],
    "costs": [cost_{a} for a in 1,...,A],
    "max_clicks": [max_click_{a} for a in 1,...,A],
    "unique_clicks": [unique_click_{a} for a in 1,...,A],
    "budget": budget
}

OBJECTIVE: How many clicks from each ad type should Custom Tees purchase to maximize the number of unique clicks within the budget?

OUTPUT INFO:

- the number of clicks purchased for each ad type is \var{clicks_{a}} in thousands.
- \var{total_unique_clicks} represents the total number of unique clicks.

OUTPUT FORMAT:

{
    "clicks": [click_{a} for a in 1, ..., A],
    "total_unique_clicks": total_unique_clicks
}
</DESCRIPTION>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300,
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120],
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

#### Extract data from JSON
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

#### Number of ad types
A = len(young_clicks)

#### Define the LP problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Define decision variables
clicks = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

#### Objective function: maximize total unique clicks
total_unique_clicks = pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)])
problem += total_unique_clicks, "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum([clicks[a] * costs[a] for a in range(A)]) <= budget, "Budget_Constraint"
problem += pulp.lpSum([clicks[a] * young_clicks[a] / 1000 for a in range(A)]) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * old_clicks[a] / 1000 for a in range(A)]) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)]) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum([clicks[a] * unique_clicks[a] / 1000 for a in range(A)]) >= goal_unique_old, "Unique_Old_Clicks_Constraint"

#### Solve the problem
problem.solve()

#### Prepare output
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks_result = pulp.value(problem.objective)

#### Output the results
output = {
    "clicks": clicks_result,
    "total_unique_clicks": total_unique_clicks_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

