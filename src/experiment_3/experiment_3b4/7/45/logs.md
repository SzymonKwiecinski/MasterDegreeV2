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
To solve this problem, we need to formulate a linear programming (LP) model to minimize the cost of the ad campaign while satisfying the constraints related to clicks and unique clicks from different age groups. Let's denote the number of thousands of clicks purchased from ad type \( a \) as \( x_a \).

Here's the formulation of the LP model:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Ad Campaign}

\subsection*{Decision Variables:}
\begin{align*}
x_a &: \text{Number of thousands of clicks purchased from ad type } a,\ a = 1, \ldots, A.
\end{align*}

\subsection*{Objective Function:}
Minimize the total cost of the ad campaign:
\[
\text{Minimize } \sum_{a=1}^{A} \text{cost}_{a} \times x_a
\]

\subsection*{Constraints:}

1. Total clicks from the 18-25 age group:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \times x_a \geq \text{goal\_young}
\]

2. Total clicks from the age group older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \times x_a \geq \text{goal\_old}
\]

3. Total unique clicks from the 18-25 age group:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_a \geq \text{goal\_unique\_young}
\]

4. Total unique clicks from the age group older than 25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_{a},\ \forall a = 1, \ldots, A
\]

\end{document}
```

In this model, the objective function minimizes the total cost by summing over all ad types, considering their respective costs. The constraints ensure that the company meets the required number of clicks and unique clicks from each age group, as well as sticking to the maximum allowable clicks for each ad type. The decision variables \( x_a \) represent how many thousands of clicks to purchase for each ad type.

The solution to this LP model will provide the number of clicks to purchase for each ad type and the total cost of the ad campaign.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Ad Campaign}

\subsection*{Decision Variables:}
\begin{align*}
x_a &: \text{Number of thousands of clicks purchased from ad type } a,\ a = 1, \ldots, A.
\end{align*}

\subsection*{Objective Function:}
Minimize the total cost of the ad campaign:
\[
\text{Minimize } \sum_{a=1}^{A} \text{cost}_{a} \times x_a
\]

\subsection*{Constraints:}

1. Total clicks from the 18-25 age group:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \times x_a \geq \text{goal\_young}
\]

2. Total clicks from the age group older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \times x_a \geq \text{goal\_old}
\]

3. Total unique clicks from the 18-25 age group:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{young\_click}_{a} \times x_a \geq \text{goal\_unique\_young}
\]

4. Total unique clicks from the age group older than 25:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \times \text{old\_click}_{a} \times x_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_{a},\ \forall a = 1, \ldots, A
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the provided JSON
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

#### Number of ad types
ad_types = len(data['costs'])

#### Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

#### Decision variables
x = [pulp.LpVariable(f"x_{a}", lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(ad_types)]

#### Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(ad_types))

#### Constraints
#### 1. Total clicks from the 18-25 age group
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_young']

#### 2. Total clicks from the age group older than 25
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_old']

#### 3. Total unique clicks from the 18-25 age group
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_unique_young']

#### 4. Total unique clicks from the age group older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(ad_types)) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

