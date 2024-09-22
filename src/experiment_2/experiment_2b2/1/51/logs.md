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
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value

#### Data from the problem
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

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

A = len(young_clicks)  #### Number of ad types

#### Create a problem variable
problem = LpProblem("Ad_Campaign_Optimization", LpMaximize)

#### Decision variables
clicks = [LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a]) for a in range(A)]

#### Objective function: Maximize unique clicks
problem += lpSum(unique_clicks[a] * clicks[a] for a in range(A))

#### Constraints
#### Total number of young clicks target
problem += lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young

#### Total number of old clicks target
problem += lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old

#### Total number of unique young clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (young_clicks[a]/100) for a in range(A)) >= goal_unique_young

#### Total number of unique old clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (old_clicks[a]/100) for a in range(A)) >= goal_unique_old

#### Budget constraint
problem += lpSum(costs[a] * clicks[a] for a in range(A)) <= budget

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "clicks": [clicks[a].varValue for a in range(A)],
    "total_unique_clicks": value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

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
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value

#### Data from the problem
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

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

A = len(young_clicks)  #### Number of ad types

#### Create a problem variable
problem = LpProblem("Ad_Campaign_Optimization", LpMaximize)

#### Decision variables
clicks = [LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a]) for a in range(A)]

#### Objective function: Maximize unique clicks
problem += lpSum(unique_clicks[a] * clicks[a] for a in range(A))

#### Constraints
#### Total number of young clicks target
problem += lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young

#### Total number of old clicks target
problem += lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old

#### Total number of unique young clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (young_clicks[a]/100) for a in range(A)) >= goal_unique_young

#### Total number of unique old clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (old_clicks[a]/100) for a in range(A)) >= goal_unique_old

#### Budget constraint
problem += lpSum(costs[a] * clicks[a] for a in range(A)) <= budget

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "clicks": [clicks[a].varValue for a in range(A)],
    "total_unique_clicks": value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

## START MESSAGE 2 
### ROLE: Role.USER
Fix the code based on the error

## START MESSAGE 3 
### ROLE: Role.USER
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_2/experiment_2b2/1/51/python_code0.py", line 56, in <module>
    print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
                                      ^^^^
NameError: name 'pulp' is not defined
</CODE_ERROR>


## START MESSAGE 4 
### ROLE: Role.ASSISTANT
```python
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, value

#### Data from the problem
data = {'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 
        'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 
        'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}

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

A = len(young_clicks)  #### Number of ad types

#### Create a problem variable
problem = LpProblem("Ad_Campaign_Optimization", LpMaximize)

#### Decision variables
clicks = [LpVariable(f'clicks_{a}', lowBound=0, upBound=max_clicks[a]) for a in range(A)]

#### Objective function: Maximize unique clicks
problem += lpSum(unique_clicks[a] * clicks[a] for a in range(A))

#### Constraints
#### Total number of young clicks target
problem += lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young

#### Total number of old clicks target
problem += lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old

#### Total number of unique young clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (young_clicks[a]/100) for a in range(A)) >= goal_unique_young

#### Total number of unique old clicks target
problem += lpSum(unique_clicks[a] * clicks[a] * (old_clicks[a]/100) for a in range(A)) >= goal_unique_old

#### Budget constraint
problem += lpSum(costs[a] * clicks[a] for a in range(A)) <= budget

#### Solve the problem
problem.solve()

#### Prepare the output
output = {
    "clicks": [clicks[a].varValue for a in range(A)],
    "total_unique_clicks": value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
```

