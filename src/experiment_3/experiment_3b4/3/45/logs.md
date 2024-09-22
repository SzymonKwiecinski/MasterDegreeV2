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
To solve this problem using Linear Programming, we need to define a mathematical model that captures the constraints and the objective to minimize the cost. Here's the latex representation of the problem:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Decision Variables}
Let \( \text{clicks}_a \) be the number of thousands of clicks purchased for ad type \( a \) where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost of the ad campaign:
\[
\text{Minimize} \quad \sum_{a=1}^{A} \text{cost}_a \times \text{clicks}_a
\]

\subsection*{Constraints}

1. Goal for clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \times \text{clicks}_a \geq \text{goal\_young}
\]

2. Goal for clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \times \text{clicks}_a \geq \text{goal\_old}
\]

3. Goal for unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_{a} \times \text{young\_click}_{a} \right) \times \text{clicks}_a \geq \text{goal\_unique\_young}
\]

4. Goal for unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_{a} \times \text{old\_click}_{a} \right) \times \text{clicks}_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
\text{clicks}_a \leq \text{max\_click}_{a}, \quad \forall a = 1, 2, \ldots, A
\]

6. Non-negativity constraints:
\[
\text{clicks}_a \geq 0, \quad \forall a = 1, 2, \ldots, A
\]

\subsection*{Parameters}
\begin{align*}
\text{age group click percentages:} & \quad \text{young\_click}_{a}, \text{old\_click}_{a} \\
\text{cost per 1000 clicks:} & \quad \text{cost}_{a} \\
\text{maximum clicks:} & \quad \text{max\_click}_{a} \\
\text{unique click percentages:} & \quad \text{unique\_click}_{a}
\end{align*}

\end{document}
```

The above document defines the decision variables, objective function, and constraints for the Linear Programming model, which determines how many clicks to purchase from each ad type to achieve the desired click goals while minimizing costs.

# START: PY_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Based on mathematical model provided in Latex format you are creating a python script in Pulp library. You get also data in json format between: <DATA></DATA> Do not include 'pip install' in script. Assume every python package is installed. Do not use `while` loop in python code! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<MATH_MODEL>
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Decision Variables}
Let \( \text{clicks}_a \) be the number of thousands of clicks purchased for ad type \( a \) where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost of the ad campaign:
\[
\text{Minimize} \quad \sum_{a=1}^{A} \text{cost}_a \times \text{clicks}_a
\]

\subsection*{Constraints}

1. Goal for clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \times \text{clicks}_a \geq \text{goal\_young}
\]

2. Goal for clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \times \text{clicks}_a \geq \text{goal\_old}
\]

3. Goal for unique clicks from visitors aged 18-25:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_{a} \times \text{young\_click}_{a} \right) \times \text{clicks}_a \geq \text{goal\_unique\_young}
\]

4. Goal for unique clicks from visitors older than 25:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_{a} \times \text{old\_click}_{a} \right) \times \text{clicks}_a \geq \text{goal\_unique\_old}
\]

5. Maximum allowable clicks for each ad type:
\[
\text{clicks}_a \leq \text{max\_click}_{a}, \quad \forall a = 1, 2, \ldots, A
\]

6. Non-negativity constraints:
\[
\text{clicks}_a \geq 0, \quad \forall a = 1, 2, \ldots, A
\]

\subsection*{Parameters}
\begin{align*}
\text{age group click percentages:} & \quad \text{young\_click}_{a}, \text{old\_click}_{a} \\
\text{cost per 1000 clicks:} & \quad \text{cost}_{a} \\
\text{maximum clicks:} & \quad \text{max\_click}_{a} \\
\text{unique click percentages:} & \quad \text{unique\_click}_{a}
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
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
A = len(data['costs'])

#### Define the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

#### Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

#### Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A))

#### Constraints
#### 1. Goal for clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

#### 2. Goal for clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

#### 3. Goal for unique clicks from visitors aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']

#### 4. Goal for unique clicks from visitors older than 25
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

#### Display individual decision variable values
for a in range(A):
    print(f'Clicks for ad type {a + 1}: {clicks[a].varValue}')
```

