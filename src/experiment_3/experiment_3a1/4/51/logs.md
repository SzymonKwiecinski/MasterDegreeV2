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

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\textbf{Indices:}
\begin{itemize}
    \item $a$: Index for ad types, where $a = 1, \ldots, A$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $goal\_young$: Target clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Target clicks from visitors older than 25 (in thousands)
    \item $goal\_unique\_young$: Target unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Target unique clicks from visitors older than 25 (in thousands)
    \item $young\_click_{a}$: Estimated percentage of clicks from the 18-25 age range for ad type $a$
    \item $old\_click_{a}$: Estimated percentage of clicks from older visitors for ad type $a$
    \item $cost_{a}$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_{a}$: Maximum allowable clicks (in thousands) for ad type $a$
    \item $unique\_click_{a}$: Estimated percentage of unique visitors for ad type $a$
    \item $budget$: Total advertising budget
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ (in thousands)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a}
\]

\textbf{Subject to:}
\begin{align*}
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} & \geq goal\_young \\
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} & \geq goal\_old \\
\sum_{a=1}^{A} clicks_{a} & \leq budget \\
clicks_{a} & \leq max\_click_{a}, \quad \forall a \\
clicks_{a} & \geq 0, \quad \forall a
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $clicks$: The number of clicks purchased for each ad type $a$ (in thousands)
    \item $total\_unique\_clicks$: Total number of unique clicks
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

\textbf{Indices:}
\begin{itemize}
    \item $a$: Index for ad types, where $a = 1, \ldots, A$
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $goal\_young$: Target clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Target clicks from visitors older than 25 (in thousands)
    \item $goal\_unique\_young$: Target unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Target unique clicks from visitors older than 25 (in thousands)
    \item $young\_click_{a}$: Estimated percentage of clicks from the 18-25 age range for ad type $a$
    \item $old\_click_{a}$: Estimated percentage of clicks from older visitors for ad type $a$
    \item $cost_{a}$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_{a}$: Maximum allowable clicks (in thousands) for ad type $a$
    \item $unique\_click_{a}$: Estimated percentage of unique visitors for ad type $a$
    \item $budget$: Total advertising budget
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ (in thousands)
\end{itemize}

\textbf{Objective Function:}
\[
\text{Maximize } \sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a}
\]

\textbf{Subject to:}
\begin{align*}
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} & \geq goal\_young \\
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} & \geq goal\_old \\
\sum_{a=1}^{A} clicks_{a} & \leq budget \\
clicks_{a} & \leq max\_click_{a}, \quad \forall a \\
clicks_{a} & \geq 0, \quad \forall a
\end{align*}

\textbf{Output:}
\begin{itemize}
    \item $clicks$: The number of clicks purchased for each ad type $a$ (in thousands)
    \item $total\_unique\_clicks$: Total number of unique clicks
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from provided input
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

#### Define the problem
problem = pulp.LpProblem("CustomTeesAdvertising", pulp.LpMaximize)

#### Decision Variables
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0)

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']
problem += pulp.lpSum(clicks[a] for a in range(A)) <= data['budget'] / 1000  #### converting budget to thousands
for a in range(A):
    problem += clicks[a] <= data['max_clicks'][a]

#### Solve the problem
problem.solve()

#### Output results
clicks_result = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)
print(f'Clicks Purchased: {clicks_result}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

