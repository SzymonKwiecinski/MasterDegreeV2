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
    "unique_clicks": [unique_click_{a} for a in 1,...,A]
}

OBJECTIVE: How many clicks from each ad type should Custom Tees purchase to minimize cost?

OUTPUT INFO:

- the number of clicks purchased for each ad type is \var{clicks_{a}} in thousands.
- \var{total_cost} represents the total cost of the ad campaign.

OUTPUT FORMAT:

{
    "clicks": [click_{a} for a in 1, ..., A],
    "total_cost": total_cost
}
</DESCRIPTION>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Problem data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90]
}

#### Initialize the problem
problem = pulp.LpProblem("Minimize_Advertising_Cost", pulp.LpMinimize)

#### Decision variables: Number of clicks in thousands for each ad type
A = len(data['young_clicks'])
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

#### Objective: Minimize the total cost of clicks
total_cost = pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])
problem += total_cost

#### Constraints
#### 1. Total clicks from young visitors
problem += pulp.lpSum([data['young_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_young']

#### 2. Total clicks from older visitors
problem += pulp.lpSum([data['old_clicks'][a] / 100 * clicks[a] for a in range(A)]) >= data['goal_old']

#### 3. Total unique clicks from young visitors
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)
                       if data['young_clicks'][a] / 100 * clicks[a] >= data['goal_unique_young']]) >= data['goal_unique_young']

#### 4. Total unique clicks from older visitors
problem += pulp.lpSum([data['unique_clicks'][a] / 100 * clicks[a] for a in range(A)
                       if data['old_clicks'][a] / 100 * clicks[a] >= data['goal_unique_old']]) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Prepare the output
solution = {
    "clicks": [pulp.value(clicks[a]) for a in range(A)],
    "total_cost": pulp.value(total_cost)
}

#### Print the solution
print(f'Solution: {solution}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

