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

\section*{Problem Formulation}

Custom Tees is planning an online advertising campaign with \( A \) different ad types. The goal is to maximize the number of unique clicks within a given budget while satisfying certain constraints related to age demographics and unique clicks.

\subsection*{Parameters}
\begin{align*}
    \text{Let } A & \text{ be the number of ad types.} \\
    \text{Let } \text{goal\_young} & \text{ be the goal of thousand clicks from visitors aged 18-25.} \\
    \text{Let } \text{goal\_old} & \text{ be the goal of thousand clicks from visitors older than 25.} \\
    \text{Let } \text{goal\_unique\_young} & \text{ be the goal of thousand unique clicks from visitors aged 18-25.} \\
    \text{Let } \text{goal\_unique\_old} & \text{ be the goal of thousand unique clicks from visitors older than 25.} \\
    \text{Let } \text{young\_clicks}_{a} & \text{ be the estimated percentage of clicks from the 18-25 age range for ad type } a. \\
    \text{Let } \text{old\_clicks}_{a} & \text{ be the estimated percentage of clicks from older visitors for ad type } a. \\
    \text{Let } \text{cost}_{a} & \text{ be the cost of ad type } a \text{ per 1000 clicks.} \\
    \text{Let } \text{max\_clicks}_{a} & \text{ be the maximum allowable clicks for ad type } a \text{ in thousands.} \\
    \text{Let } \text{unique\_clicks}_{a} & \text{ be the estimated percentage of unique visitors for ad type } a. \\
    \text{Let } \text{budget} & \text{ be the total advertising budget.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{Let } x_{a} & \text{ be the number of clicks purchased for each ad type } a \text{ in thousands.}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\max \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a}
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} \text{cost}_{a} \times x_{a} \leq \text{budget} & \text{(Budget constraint)} \\
    & \sum_{a=1}^{A} \text{young\_clicks}_{a} \times x_{a} \geq \text{goal\_young} & \text{(Young clicks constraint)} \\
    & \sum_{a=1}^{A} \text{old\_clicks}_{a} \times x_{a} \geq \text{goal\_old} & \text{(Old clicks constraint)} \\
    & \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a} \geq \text{goal\_unique\_young} & \text{(Unique young clicks constraint)} \\
    & \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a} \geq \text{goal\_unique\_old} & \text{(Unique old clicks constraint)} \\
    & 0 \leq x_{a} \leq \text{max\_clicks}_{a} & \text{for all } a = 1, \ldots, A.
\end{align*}

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

\section*{Problem Formulation}

Custom Tees is planning an online advertising campaign with \( A \) different ad types. The goal is to maximize the number of unique clicks within a given budget while satisfying certain constraints related to age demographics and unique clicks.

\subsection*{Parameters}
\begin{align*}
    \text{Let } A & \text{ be the number of ad types.} \\
    \text{Let } \text{goal\_young} & \text{ be the goal of thousand clicks from visitors aged 18-25.} \\
    \text{Let } \text{goal\_old} & \text{ be the goal of thousand clicks from visitors older than 25.} \\
    \text{Let } \text{goal\_unique\_young} & \text{ be the goal of thousand unique clicks from visitors aged 18-25.} \\
    \text{Let } \text{goal\_unique\_old} & \text{ be the goal of thousand unique clicks from visitors older than 25.} \\
    \text{Let } \text{young\_clicks}_{a} & \text{ be the estimated percentage of clicks from the 18-25 age range for ad type } a. \\
    \text{Let } \text{old\_clicks}_{a} & \text{ be the estimated percentage of clicks from older visitors for ad type } a. \\
    \text{Let } \text{cost}_{a} & \text{ be the cost of ad type } a \text{ per 1000 clicks.} \\
    \text{Let } \text{max\_clicks}_{a} & \text{ be the maximum allowable clicks for ad type } a \text{ in thousands.} \\
    \text{Let } \text{unique\_clicks}_{a} & \text{ be the estimated percentage of unique visitors for ad type } a. \\
    \text{Let } \text{budget} & \text{ be the total advertising budget.}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    \text{Let } x_{a} & \text{ be the number of clicks purchased for each ad type } a \text{ in thousands.}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\max \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a}
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} \text{cost}_{a} \times x_{a} \leq \text{budget} & \text{(Budget constraint)} \\
    & \sum_{a=1}^{A} \text{young\_clicks}_{a} \times x_{a} \geq \text{goal\_young} & \text{(Young clicks constraint)} \\
    & \sum_{a=1}^{A} \text{old\_clicks}_{a} \times x_{a} \geq \text{goal\_old} & \text{(Old clicks constraint)} \\
    & \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a} \geq \text{goal\_unique\_young} & \text{(Unique young clicks constraint)} \\
    & \sum_{a=1}^{A} \text{unique\_clicks}_{a} \times x_{a} \geq \text{goal\_unique\_old} & \text{(Unique old clicks constraint)} \\
    & 0 \leq x_{a} \leq \text{max\_clicks}_{a} & \text{for all } a = 1, \ldots, A.
\end{align*}

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
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a]) for a in range(A)]

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A))

#### Constraints
#### Budget constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget']

#### Young clicks constraint
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young']

#### Old clicks constraint
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old']

#### Unique young clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young']

#### Unique old clicks constraint
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


