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

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Variables}
Let \( x_a \) represent the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_old} \): Target clicks from visitors older than 25 (in thousands).
    \item \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (in thousands).
    \item \( \text{young\_click}_a \): Percentage of clicks from age 18-25 for ad type \( a \).
    \item \( \text{old\_click}_a \): Percentage of clicks from age over 25 for ad type \( a \).
    \item \( \text{cost}_a \): Cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_a \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item \( \text{unique\_click}_a \): Estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \): Total advertising budget.
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize} \quad Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} ( \text{young\_click}_a \cdot x_a ) \geq \text{goal\_young} \quad & \text{(Clicks from 18-25)} \\
    & \sum_{a=1}^{A} ( \text{old\_click}_a \cdot x_a ) \geq \text{goal\_old} \quad & \text{(Clicks from older than 25)} \\
    & \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young} + \text{goal\_unique\_old} \quad & \text{(Unique clicks)} \\
    & \sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget} \quad & \text{(Budget constraint)} \\
    & 0 \leq x_a \leq \text{max\_click}_a \quad & \text{for } a = 1, \ldots, A \quad \text{(Max clicks for each ad type)}
\end{align*}

\subsection*{Output}
The output will be:
\begin{align*}
    \text{clicks} &= [x_1, x_2, \ldots, x_A] \\
    \text{total\_unique\_clicks} &= Z
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

\section*{Linear Programming Model for Custom Tees Online Advertising Campaign}

\subsection*{Variables}
Let \( x_a \) represent the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_old} \): Target clicks from visitors older than 25 (in thousands).
    \item \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (in thousands).
    \item \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (in thousands).
    \item \( \text{young\_click}_a \): Percentage of clicks from age 18-25 for ad type \( a \).
    \item \( \text{old\_click}_a \): Percentage of clicks from age over 25 for ad type \( a \).
    \item \( \text{cost}_a \): Cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_a \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item \( \text{unique\_click}_a \): Estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \): Total advertising budget.
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize} \quad Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} ( \text{young\_click}_a \cdot x_a ) \geq \text{goal\_young} \quad & \text{(Clicks from 18-25)} \\
    & \sum_{a=1}^{A} ( \text{old\_click}_a \cdot x_a ) \geq \text{goal\_old} \quad & \text{(Clicks from older than 25)} \\
    & \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young} + \text{goal\_unique\_old} \quad & \text{(Unique clicks)} \\
    & \sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget} \quad & \text{(Budget constraint)} \\
    & 0 \leq x_a \leq \text{max\_click}_a \quad & \text{for } a = 1, \ldots, A \quad \text{(Max clicks for each ad type)}
\end{align*}

\subsection*{Output}
The output will be:
\begin{align*}
    \text{clicks} &= [x_1, x_2, \ldots, x_A] \\
    \text{total\_unique\_clicks} &= Z
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Constants and data from the JSON
goal_young = 500
goal_old = 600
goal_unique_young = 250
goal_unique_old = 300
young_clicks = [40, 30, 70]
old_clicks = [60, 70, 30]
costs = [75, 100, 120]
max_clicks = [600, 300, 300]
unique_clicks = [40, 75, 90]
budget = 105000

#### Number of ad types
A = len(young_clicks)

#### Define the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Define decision variables
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=max_clicks[a], cat='Continuous') for a in range(A)]

#### Objective function
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * x[a] for a in range(A)) >= goal_young, "Young_Clicks_Target"
problem += pulp.lpSum(old_clicks[a] * x[a] for a in range(A)) >= goal_old, "Old_Clicks_Target"
problem += pulp.lpSum(unique_clicks[a] * x[a] for a in range(A)) >= (goal_unique_young + goal_unique_old), "Unique_Clicks_Target"
problem += pulp.lpSum(costs[a] * x[a] for a in range(A)) <= budget, "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Results
clicks = [pulp.value(x_var) for x_var in x]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks (in thousands) for each ad type: {clicks}')
print(f'Total Unique Clicks (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')
```


