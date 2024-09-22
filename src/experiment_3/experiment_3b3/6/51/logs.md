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

\section*{Linear Programming Model for Advertising Campaign}

\textbf{Definitions:}
\begin{itemize}
    \item Let \( A \) be the number of different ad types.
    \item Let \( goal\_young \) be the goal of clicks from visitors aged 18-25 (in thousands).
    \item Let \( goal\_old \) be the goal of clicks from visitors older than 25 (in thousands).
    \item Let \( goal\_unique\_young \) be the goal of unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( goal\_unique\_old \) be the goal of unique clicks from visitors older than 25 (in thousands).
    \item Let \( young\_click_a \) be the percentage of clicks from the 18-25 age range for ad type \( a \).
    \item Let \( old\_click_a \) be the percentage of clicks from older visitors for ad type \( a \).
    \item Let \( cost_a \) be the cost per 1000 clicks for ad type \( a \).
    \item Let \( max\_click_a \) be the maximum allowable clicks (in thousands) for ad type \( a \).
    \item Let \( unique\_click_a \) be the estimated percentage of unique visitors for ad type \( a \).
    \item Let \( budget \) be the total advertising budget.
    \item Let \( clicks_a \) be the number of clicks purchased for ad type \( a \) (in thousands).
    \item Let \( total\_unique\_clicks \) be the total number of unique clicks.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } total\_unique\_clicks = \sum_{a=1}^{A} unique\_click_a \cdot clicks_a
\]

\textbf{Subject to:}
\[
\sum_{a=1}^{A} young\_click_a \cdot clicks_a \geq goal\_young
\]
\[
\sum_{a=1}^{A} old\_click_a \cdot clicks_a \geq goal\_old
\]
\[
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a \geq goal\_unique\_young + goal\_unique\_old
\]
\[
\sum_{a=1}^{A} cost_a \cdot clicks_a \leq budget
\]
\[
clicks_a \leq max\_click_a \quad \forall a = 1, \ldots, A
\]
\[
clicks_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\textbf{Output:}
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( clicks = [clicks_a \text{ for } a \text{ in } 1, \ldots, A] \)
    \item Total unique clicks: \( total\_unique\_clicks \)
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

\section*{Linear Programming Model for Advertising Campaign}

\textbf{Definitions:}
\begin{itemize}
    \item Let \( A \) be the number of different ad types.
    \item Let \( goal\_young \) be the goal of clicks from visitors aged 18-25 (in thousands).
    \item Let \( goal\_old \) be the goal of clicks from visitors older than 25 (in thousands).
    \item Let \( goal\_unique\_young \) be the goal of unique clicks from visitors aged 18-25 (in thousands).
    \item Let \( goal\_unique\_old \) be the goal of unique clicks from visitors older than 25 (in thousands).
    \item Let \( young\_click_a \) be the percentage of clicks from the 18-25 age range for ad type \( a \).
    \item Let \( old\_click_a \) be the percentage of clicks from older visitors for ad type \( a \).
    \item Let \( cost_a \) be the cost per 1000 clicks for ad type \( a \).
    \item Let \( max\_click_a \) be the maximum allowable clicks (in thousands) for ad type \( a \).
    \item Let \( unique\_click_a \) be the estimated percentage of unique visitors for ad type \( a \).
    \item Let \( budget \) be the total advertising budget.
    \item Let \( clicks_a \) be the number of clicks purchased for ad type \( a \) (in thousands).
    \item Let \( total\_unique\_clicks \) be the total number of unique clicks.
\end{itemize}

\textbf{Objective:}
\[
\text{Maximize } total\_unique\_clicks = \sum_{a=1}^{A} unique\_click_a \cdot clicks_a
\]

\textbf{Subject to:}
\[
\sum_{a=1}^{A} young\_click_a \cdot clicks_a \geq goal\_young
\]
\[
\sum_{a=1}^{A} old\_click_a \cdot clicks_a \geq goal\_old
\]
\[
\sum_{a=1}^{A} unique\_click_a \cdot clicks_a \geq goal\_unique\_young + goal\_unique\_old
\]
\[
\sum_{a=1}^{A} cost_a \cdot clicks_a \leq budget
\]
\[
clicks_a \leq max\_click_a \quad \forall a = 1, \ldots, A
\]
\[
clicks_a \geq 0 \quad \forall a = 1, \ldots, A
\]

\textbf{Output:}
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( clicks = [clicks_a \text{ for } a \text{ in } 1, \ldots, A] \)
    \item Total unique clicks: \( total\_unique\_clicks \)
\end{itemize}

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
A = len(data['young_clicks'])

#### Problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMaximize)

#### Decision variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, cat='Continuous') for a in range(A)]

#### Objective function
total_unique_clicks = pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))
problem += total_unique_clicks

#### Constraints
#### Goal of clicks from visitors aged 18-25
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']

#### Goal of clicks from visitors older than 25
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']

#### Goal of unique clicks
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= (data['goal_unique_young'] + data['goal_unique_old'])

#### Budget constraint
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

#### Maximum allowable clicks for each ad type
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

#### Solve the problem
problem.solve()

#### Output the results
results = [pulp.value(clicks[a]) for a in range(A)]
print(f'Clicks purchased for each ad type: {results}')
print(f'Total unique clicks (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

