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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Parameters}
\begin{itemize}
    \item $A$: Number of different ad types
    \item $goal\_young$: Goal for clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Goal for clicks from visitors aged 25 and older (in thousands)
    \item $goal\_unique\_young$: Goal for unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Goal for unique clicks from visitors aged 25 and older (in thousands)
    \item $young\_click_a$: Percentage of clicks from the 18-25 age range for ad type $a$
    \item $old\_click_a$: Percentage of clicks from older visitors for ad type $a$
    \item $cost_a$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_a$: Maximum allowable clicks for ad type $a$ (in thousands)
    \item $unique\_click_a$: Estimated percentage of unique visitors for ad type $a$
\end{itemize}

\subsection*{Decision Variables}
Let $clicks_a$ be the number of clicks purchased for ad type $a$ (in thousands) for $a = 1, \ldots, A$.

\subsection*{Objective}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{a=1}^{A} cost_a \cdot clicks_a
\]

\subsection*{Constraints}
\begin{align*}
\sum_{a=1}^{A} young\_click_a \cdot clicks_a & \geq goal\_young \\
\sum_{a=1}^{A} old\_click_a \cdot clicks_a & \geq goal\_old \\
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a & \geq goal\_unique\_young \\
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a & \geq goal\_unique\_old \\
clicks_a & \leq max\_click_a \quad \forall a = 1, \ldots, A \\
clicks_a & \geq 0 \quad \forall a = 1, \ldots, A
\end{align*}

\subsection*{Output}
The output will be as follows:
\begin{itemize}
    \item $clicks = [clicks_a \text{ for } a = 1, \ldots, A]$
    \item $total\_cost = Z$
\end{itemize}

\end{document}
```

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

\subsection*{Parameters}
\begin{itemize}
    \item $A$: Number of different ad types
    \item $goal\_young$: Goal for clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Goal for clicks from visitors aged 25 and older (in thousands)
    \item $goal\_unique\_young$: Goal for unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Goal for unique clicks from visitors aged 25 and older (in thousands)
    \item $young\_click_a$: Percentage of clicks from the 18-25 age range for ad type $a$
    \item $old\_click_a$: Percentage of clicks from older visitors for ad type $a$
    \item $cost_a$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_a$: Maximum allowable clicks for ad type $a$ (in thousands)
    \item $unique\_click_a$: Estimated percentage of unique visitors for ad type $a$
\end{itemize}

\subsection*{Decision Variables}
Let $clicks_a$ be the number of clicks purchased for ad type $a$ (in thousands) for $a = 1, \ldots, A$.

\subsection*{Objective}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{a=1}^{A} cost_a \cdot clicks_a
\]

\subsection*{Constraints}
\begin{align*}
\sum_{a=1}^{A} young\_click_a \cdot clicks_a & \geq goal\_young \\
\sum_{a=1}^{A} old\_click_a \cdot clicks_a & \geq goal\_old \\
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a & \geq goal\_unique\_young \\
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a & \geq goal\_unique\_old \\
clicks_a & \leq max\_click_a \quad \forall a = 1, \ldots, A \\
clicks_a & \geq 0 \quad \forall a = 1, \ldots, A
\end{align*}

\subsection*{Output}
The output will be as follows:
\begin{itemize}
    \item $clicks = [clicks_a \text{ for } a = 1, \ldots, A]$
    \item $total\_cost = Z$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON
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
A = len(data['young_clicks'])

#### Initialize the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

#### Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

#### Objective Function
problem += pulp.lpSum([data['costs'][a] * clicks[a] for a in range(A)])

#### Constraints
#### Young age group clicks
problem += pulp.lpSum([data['young_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_young']

#### Old age group clicks
problem += pulp.lpSum([data['old_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_old']

#### Unique young clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_young']

#### Unique old clicks
problem += pulp.lpSum([data['unique_clicks'][a] * clicks[a] for a in range(A)]) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Output the solution
clicks_result = [pulp.value(clicks[a]) for a in range(A)]
total_cost = pulp.value(problem.objective)

print("Clicks per ad type:")
for a in range(A):
    print(f"Ad Type {a + 1}: {clicks_result[a]:.2f} thousand clicks")
print(f"Total Cost: {total_cost:.2f}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

