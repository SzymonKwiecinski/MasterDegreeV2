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
To solve this problem, we need to create a linear programming model that minimizes the total cost of the advertising campaign while satisfying the click requirements from different age groups and ensuring uniqueness in clicks. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Decision Variables}
Let \( x_a \) be the number of thousands of clicks purchased for ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\subsection*{Constraints}

1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_a \quad \forall a = 1, \ldots, A
\]

\subsection*{Non-negativity Constraints}
\[
x_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\end{document}
```

This linear programming model aims to determine the optimal number of clicks \( x_a \) for each ad type \( a \) to minimize the total cost while meeting all constraints related to age-specific and unique click goals, along with the maximum allowable clicks for each ad type.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Decision Variables}
Let \( x_a \) be the number of thousands of clicks purchased for ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\subsection*{Constraints}

1. Clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

2. Clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

3. Unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

4. Unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_a \quad \forall a = 1, \ldots, A
\]

\subsection*{Non-negativity Constraints}
\[
x_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


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
    'unique_clicks': [40, 75, 90]
}

#### Unpack data
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

#### Number of ad types
A = len(costs)

#### Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

#### Objective function
problem += pulp.lpSum([costs[a] * x[a] for a in range(A)])

#### Constraints

#### Clicks from visitors aged 18-25
problem += pulp.lpSum([young_clicks[a] * x[a] for a in range(A)]) >= goal_young

#### Clicks from visitors older than 25
problem += pulp.lpSum([old_clicks[a] * x[a] for a in range(A)]) >= goal_old

#### Unique clicks from visitors aged 18-25
problem += pulp.lpSum([young_clicks[a] * unique_clicks[a] * x[a] for a in range(A)]) >= goal_unique_young

#### Unique clicks from visitors older than 25
problem += pulp.lpSum([old_clicks[a] * unique_clicks[a] * x[a] for a in range(A)]) >= goal_unique_old

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

