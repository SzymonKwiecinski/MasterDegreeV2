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
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_a \) be the number of clicks purchased from ad type \( a \) (in thousands), for \( a = 1, 2, \ldots, A \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{goal\_young} \): goal of clicks from visitors aged 18-25 (in thousands)
    \item \( \text{goal\_old} \): goal of clicks from visitors older than 25 (in thousands)
    \item \( \text{goal\_unique\_young} \): goal of unique clicks from visitors aged 18-25 (in thousands)
    \item \( \text{goal\_unique\_old} \): goal of unique clicks from visitors older than 25 (in thousands)
    \item \( \text{young\_click}_{a} \): percentage of clicks from the 18-25 age range for ad type \( a \)
    \item \( \text{old\_click}_{a} \): percentage of clicks from older visitors for ad type \( a \)
    \item \( \text{cost}_{a} \): cost per 1000 clicks for ad type \( a \)
    \item \( \text{max\_click}_{a} \): maximum allowable clicks for ad type \( a \) (in thousands)
    \item \( \text{unique\_click}_{a} \): estimated percentage of unique visitors for ad type \( a \)
    \item \( \text{budget} \): total advertising budget
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a
\]

\textbf{Subject to:}

\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a & \geq \text{goal\_young} \\
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a & \geq \text{goal\_old} \\
\sum_{a=1}^{A} x_a & \leq \text{budget} \\
x_a & \leq \text{max\_click}_{a} \quad \text{for } a = 1, 2, \ldots, A \\
x_a & \geq 0 \quad \text{for } a = 1, 2, \ldots, A
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( x_a \) (in thousands)
    \item Total unique clicks: \( Z \)
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

\section*{Linear Programming Model}

\textbf{Variables:}
\begin{itemize}
    \item Let \( x_a \) be the number of clicks purchased from ad type \( a \) (in thousands), for \( a = 1, 2, \ldots, A \).
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item \( \text{goal\_young} \): goal of clicks from visitors aged 18-25 (in thousands)
    \item \( \text{goal\_old} \): goal of clicks from visitors older than 25 (in thousands)
    \item \( \text{goal\_unique\_young} \): goal of unique clicks from visitors aged 18-25 (in thousands)
    \item \( \text{goal\_unique\_old} \): goal of unique clicks from visitors older than 25 (in thousands)
    \item \( \text{young\_click}_{a} \): percentage of clicks from the 18-25 age range for ad type \( a \)
    \item \( \text{old\_click}_{a} \): percentage of clicks from older visitors for ad type \( a \)
    \item \( \text{cost}_{a} \): cost per 1000 clicks for ad type \( a \)
    \item \( \text{max\_click}_{a} \): maximum allowable clicks for ad type \( a \) (in thousands)
    \item \( \text{unique\_click}_{a} \): estimated percentage of unique visitors for ad type \( a \)
    \item \( \text{budget} \): total advertising budget
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a
\]

\textbf{Subject to:}

\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a & \geq \text{goal\_young} \\
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a & \geq \text{goal\_old} \\
\sum_{a=1}^{A} x_a & \leq \text{budget} \\
x_a & \leq \text{max\_click}_{a} \quad \text{for } a = 1, 2, \ldots, A \\
x_a & \geq 0 \quad \text{for } a = 1, 2, \ldots, A
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( x_a \) (in thousands)
    \item Total unique clicks: \( Z \)
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data in JSON format
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

#### Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
budget = data['budget']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']

#### Number of ad types
A = len(young_clicks)

#### Create the problem
problem = pulp.LpProblem("Ad_Clicks_Optimization", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0, upBound=None)

#### Objective Function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Requirement"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Requirement"
problem += pulp.lpSum(x[a] for a in range(A)) <= budget, "Budget_Constraint"
for a in range(A):
    problem += x[a] <= max_clicks[a], f"Max_Clicks_{a}"

#### Solve the problem
problem.solve()

#### Output results
for a in range(A):
    print(f'Clicks purchased for ad type {a+1}: {x[a].varValue} (in thousands)')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

