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


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
To model this problem as a linear programming (LP) problem, our goal is to maximize the total number of unique clicks while satisfying the given constraints such as budget, age-specific click requirements, and maximum allowable clicks for each ad type.

Here is the mathematical model for the problem in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
Let \( x_a \) be the number of thousands of clicks purchased for ad type \( a \) for \( a = 1, \ldots, A \).

\textbf{Objective:}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a
\]

\textbf{Subject to the following constraints:}

1. Budget Constraint:
\[
\sum_{a=1}^{A} \text{cost}_{a} \cdot x_a \leq \text{budget}
\]

2. Age-specific Click Constraints:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young}
\]
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old}
\]

3. Unique Click Constraints for Each Age Group:
\[
\sum_{a=1}^{A} \left( \text{young\_click}_{a} \cdot \text{unique\_click}_{a} \right) \cdot x_a \geq \text{goal\_unique\_young}
\]
\[
\sum_{a=1}^{A} \left( \text{old\_click}_{a} \cdot \text{unique\_click}_{a} \right) \cdot x_a \geq \text{goal\_unique\_old}
\]

4. Maximum Allowable Clicks for Each Ad Type:
\[
0 \leq x_a \leq \text{max\_click}_{a} \quad \text{for } a = 1, \ldots, A
\]

\end{document}
```

This model includes decision variables \( x_a \) that represent the number of thousands of clicks for each ad type. The objective function aims to maximize the total unique clicks. The constraints ensure the advertising budget isn't exceeded, required clicks for specific age groups are met, unique click goals for each age group are achieved, and the number of clicks does not surpass the maximum limit for each ad type.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Decision Variables:}
Let \( x_a \) be the number of thousands of clicks purchased for ad type \( a \) for \( a = 1, \ldots, A \).

\textbf{Objective:}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a
\]

\textbf{Subject to the following constraints:}

1. Budget Constraint:
\[
\sum_{a=1}^{A} \text{cost}_{a} \cdot x_a \leq \text{budget}
\]

2. Age-specific Click Constraints:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young}
\]
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old}
\]

3. Unique Click Constraints for Each Age Group:
\[
\sum_{a=1}^{A} \left( \text{young\_click}_{a} \cdot \text{unique\_click}_{a} \right) \cdot x_a \geq \text{goal\_unique\_young}
\]
\[
\sum_{a=1}^{A} \left( \text{old\_click}_{a} \cdot \text{unique\_click}_{a} \right) \cdot x_a \geq \text{goal\_unique\_old}
\]

4. Maximum Allowable Clicks for Each Ad Type:
\[
0 \leq x_a \leq \text{max\_click}_{a} \quad \text{for } a = 1, \ldots, A
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {
    'goal_young': 500,
    'goal_old': 600,
    'goal_unique_young': 250,
    'goal_unique_old': 300,
    'young_clicks': [40, 30, 70],
    'old_clicks': [60, 70, 30],
    'costs': [75, 100, 120],
    'max_clicks': [600, 300, 300],
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

#### Number of ad types
A = len(data['unique_clicks'])

#### Initialize the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, upBound=data['max_clicks'][i]) for i in range(A)]

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][i] * x[i] for i in range(A))

#### Constraints
#### Budget constraint
problem += pulp.lpSum(data['costs'][i] * x[i] for i in range(A)) <= data['budget']

#### Age-specific click constraints
problem += pulp.lpSum(data['young_clicks'][i] * x[i] for i in range(A)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][i] * x[i] for i in range(A)) >= data['goal_old']

#### Unique click constraints for each age group
problem += pulp.lpSum(data['young_clicks'][i] * data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_young']
problem += pulp.lpSum(data['old_clicks'][i] * data['unique_clicks'][i] * x[i] for i in range(A)) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Print the optimal solution and objective value
for i in range(A):
    print(f'x_{i + 1} = {pulp.value(x[i])}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

