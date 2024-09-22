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

\subsection*{Variables}
Let \( x_a \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (thousands).
    \item \( \text{goal\_old} \): Target clicks from visitors older than 25 (thousands).
    \item \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (thousands).
    \item \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (thousands).
    \item \( \text{young\_click}_a \): Percentage of clicks from young visitors for ad type \( a \).
    \item \( \text{old\_click}_a \): Percentage of clicks from older visitors for ad type \( a \).
    \item \( \text{cost}_a \): Cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_a \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item \( \text{unique\_click}_a \): Estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \): Total advertising budget.
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right)
\]

\subsection*{Subject to Constraints}
1. Total clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{young\_click}_a \cdot x_a \right) \geq \text{goal\_young}
\]

2. Total clicks from older visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{old\_click}_a \cdot x_a \right) \geq \text{goal\_old}
\]

3. Total unique clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right) \geq \text{goal\_unique\_young}
\]

4. Total unique clicks from older visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right) \geq \text{goal\_unique\_old}
\]

5. The total cost must not exceed the budget:
\[
\sum_{a=1}^{A} \left( \text{cost}_a \cdot x_a \right) \leq \text{budget}
\]

6. Maximum clicks for each ad type:
\[
x_a \leq \text{max\_click}_a \quad \forall a
\]

7. Non-negativity constraints:
\[
x_a \geq 0 \quad \forall a
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( \{ x_a \}_{a=1}^{A} \) (in thousands).
    \item The total number of unique clicks: \( Z \).
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

\subsection*{Variables}
Let \( x_a \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{goal\_young} \): Target clicks from visitors aged 18-25 (thousands).
    \item \( \text{goal\_old} \): Target clicks from visitors older than 25 (thousands).
    \item \( \text{goal\_unique\_young} \): Target unique clicks from visitors aged 18-25 (thousands).
    \item \( \text{goal\_unique\_old} \): Target unique clicks from visitors older than 25 (thousands).
    \item \( \text{young\_click}_a \): Percentage of clicks from young visitors for ad type \( a \).
    \item \( \text{old\_click}_a \): Percentage of clicks from older visitors for ad type \( a \).
    \item \( \text{cost}_a \): Cost per 1000 clicks for ad type \( a \).
    \item \( \text{max\_click}_a \): Maximum allowable clicks for ad type \( a \) (in thousands).
    \item \( \text{unique\_click}_a \): Estimated percentage of unique visitors for ad type \( a \).
    \item \( \text{budget} \): Total advertising budget.
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right)
\]

\subsection*{Subject to Constraints}
1. Total clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{young\_click}_a \cdot x_a \right) \geq \text{goal\_young}
\]

2. Total clicks from older visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{old\_click}_a \cdot x_a \right) \geq \text{goal\_old}
\]

3. Total unique clicks from young visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right) \geq \text{goal\_unique\_young}
\]

4. Total unique clicks from older visitors must meet the goal:
\[
\sum_{a=1}^{A} \left( \text{unique\_click}_a \cdot x_a \right) \geq \text{goal\_unique\_old}
\]

5. The total cost must not exceed the budget:
\[
\sum_{a=1}^{A} \left( \text{cost}_a \cdot x_a \right) \leq \text{budget}
\]

6. Maximum clicks for each ad type:
\[
x_a \leq \text{max\_click}_a \quad \forall a
\]

7. Non-negativity constraints:
\[
x_a \geq 0 \quad \forall a
\]

\subsection*{Output}
The solution will provide:
\begin{itemize}
    \item The number of clicks purchased for each ad type: \( \{ x_a \}_{a=1}^{A} \) (in thousands).
    \item The total number of unique clicks: \( Z \).
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
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

#### Variables
x = [pulp.LpVariable(f"x_{a+1}", lowBound=0, cat='Continuous') for a in range(A)]

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
#### 1. Total clicks from young visitors
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young"

#### 2. Total clicks from older visitors
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old"

#### 3. Total unique clicks from young visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young"

#### 4. Total unique clicks from older visitors
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old"

#### 5. Total cost must not exceed the budget
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget"

#### 6. Maximum clicks for each ad type
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a+1}"

#### Solve
problem.solve()

#### Output
for a in range(A):
    print(f"Clicks for ad type {a+1} (in thousands): {x[a].varValue}")

print(f"Total unique clicks (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
```

