# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To solve the given linear programming problem, we need to define a mathematical model. Our goal is to minimize the total cost of purchasing ad clicks while meeting the specific constraints on the number of clicks from different age groups and unique visitors. Here is the mathematical formulation of the problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of the ad campaign.

Let $x_a$ be the number of clicks (in thousands) purchased for ad type $a$, where $a = 1, 2, \ldots, A$.

The total cost, $C$, is given by:
\[
C = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\textbf{Constraints:}

1. Achieve the goal for young visitors (aged 18-25):
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

2. Achieve the goal for older visitors (aged > 25):
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

3. Achieve the goal for unique young visitors:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

4. Achieve the goal for unique older visitors:
\[
\sum_{a=1}^{A} (1 - \text{unique\_click}_a) \cdot x_a \geq \text{goal\_unique\_old}
\]

5. Clicks for each ad type should not exceed the maximum allowable:
\[
0 \leq x_a \leq \text{max\_click}_a \quad \text{for all } a
\]

\textbf{Solution:}
The solution will provide the number of clicks purchased for each ad type $a$ and the total cost:
\[
\text{clicks} = [x_1, x_2, \dots, x_A]
\]
\[
\text{total\_cost} = C
\]

\end{document}
```

This linear programming formulation incorporates all the given constraints and objectives to minimize the total cost while satisfying the click requirements for both age groups and ensuring the unique click goals are met.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\textbf{Objective:} Minimize the total cost of the ad campaign.

Let $x_a$ be the number of clicks (in thousands) purchased for ad type $a$, where $a = 1, 2, \ldots, A$.

The total cost, $C$, is given by:
\[
C = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\textbf{Constraints:}

1. Achieve the goal for young visitors (aged 18-25):
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

2. Achieve the goal for older visitors (aged > 25):
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

3. Achieve the goal for unique young visitors:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

4. Achieve the goal for unique older visitors:
\[
\sum_{a=1}^{A} (1 - \text{unique\_click}_a) \cdot x_a \geq \text{goal\_unique\_old}
\]

5. Clicks for each ad type should not exceed the maximum allowable:
\[
0 \leq x_a \leq \text{max\_click}_a \quad \text{for all } a
\]

\textbf{Solution:}
The solution will provide the number of clicks purchased for each ad type $a$ and the total cost:
\[
\text{clicks} = [x_1, x_2, \dots, x_A]
\]
\[
\text{total\_cost} = C
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the problem
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

#### Define the problem
problem = pulp.LpProblem("Ad_Campaign_Cost_Minimization", pulp.LpMinimize)

#### Decision variables
A = len(data['young_clicks'])
x = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

#### Upper bounds on x
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a}"

#### Solve the problem
problem.solve()

#### Printing the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

