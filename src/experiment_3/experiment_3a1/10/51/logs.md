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

\textbf{Variables:}
\begin{itemize}
    \item Let $x_a$ be the number of clicks purchased from ad type $a$ (in thousands), for $a = 1, 2, \ldots, A$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $goal\_young$: Goal for clicks from visitors aged 18-25 (in thousands).
    \item $goal\_old$: Goal for clicks from visitors older than 25 (in thousands).
    \item $goal\_unique\_young$: Goal for unique clicks from visitors aged 18-25 (in thousands).
    \item $goal\_unique\_old$: Goal for unique clicks from visitors older than 25 (in thousands).
    \item $young\_click_a$: Estimated percentage of clicks from the 18-25 age range for ad type $a$.
    \item $old\_click_a$: Estimated percentage of clicks from older visitors for ad type $a$.
    \item $cost_a$: Cost of ad type $a$ per 1000 clicks.
    \item $max\_click_a$: Maximum allowable clicks for ad type $a$ (in thousands).
    \item $unique\_click_a$: Estimated percentage of unique visitors for ad type $a$.
    \item $budget$: Advertising budget.
\end{itemize}

\textbf{Objective Function:}
Maximize the total unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} unique\_click_a \cdot x_a
\]

\textbf{Subject to:}
1. Total clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} young\_click_a \cdot x_a \geq goal\_young
\]
2. Total clicks from old visitors must meet the goal:
\[
\sum_{a=1}^{A} old\_click_a \cdot x_a \geq goal\_old
\]
3. Total unique clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} unique\_click_a \cdot x_a \geq goal\_unique\_young
\]
4. Total unique clicks from old visitors must meet the goal:
\[
\sum_{a=1}^{A} unique\_click_a \cdot x_a \geq goal\_unique\_old
\]
5. Clicks for each ad type should not exceed the maximum allowable clicks:
\[
x_a \leq max\_click_a \quad \forall a
\]
6. The total cost of the campaign must not exceed the budget:
\[
\sum_{a=1}^{A} cost_a \cdot x_a \leq budget
\]
7. Non-negativity constraints:
\[
x_a \geq 0 \quad \forall a
\]

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

\textbf{Variables:}
\begin{itemize}
    \item Let $x_a$ be the number of clicks purchased from ad type $a$ (in thousands), for $a = 1, 2, \ldots, A$.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $goal\_young$: Goal for clicks from visitors aged 18-25 (in thousands).
    \item $goal\_old$: Goal for clicks from visitors older than 25 (in thousands).
    \item $goal\_unique\_young$: Goal for unique clicks from visitors aged 18-25 (in thousands).
    \item $goal\_unique\_old$: Goal for unique clicks from visitors older than 25 (in thousands).
    \item $young\_click_a$: Estimated percentage of clicks from the 18-25 age range for ad type $a$.
    \item $old\_click_a$: Estimated percentage of clicks from older visitors for ad type $a$.
    \item $cost_a$: Cost of ad type $a$ per 1000 clicks.
    \item $max\_click_a$: Maximum allowable clicks for ad type $a$ (in thousands).
    \item $unique\_click_a$: Estimated percentage of unique visitors for ad type $a$.
    \item $budget$: Advertising budget.
\end{itemize}

\textbf{Objective Function:}
Maximize the total unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} unique\_click_a \cdot x_a
\]

\textbf{Subject to:}
1. Total clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} young\_click_a \cdot x_a \geq goal\_young
\]
2. Total clicks from old visitors must meet the goal:
\[
\sum_{a=1}^{A} old\_click_a \cdot x_a \geq goal\_old
\]
3. Total unique clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} unique\_click_a \cdot x_a \geq goal\_unique\_young
\]
4. Total unique clicks from old visitors must meet the goal:
\[
\sum_{a=1}^{A} unique\_click_a \cdot x_a \geq goal\_unique\_old
\]
5. Clicks for each ad type should not exceed the maximum allowable clicks:
\[
x_a \leq max\_click_a \quad \forall a
\]
6. The total cost of the campaign must not exceed the budget:
\[
\sum_{a=1}^{A} cost_a \cdot x_a \leq budget
\]
7. Non-negativity constraints:
\[
x_a \geq 0 \quad \forall a
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


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
    'unique_clicks': [40, 75, 90],
    'budget': 105000
}

#### Create the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Decision variables
A = len(data['young_clicks'])
x = [pulp.LpVariable(f'x_{a}', lowBound=0, upBound=data['max_clicks'][a] / 1000) for a in range(A)]

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

