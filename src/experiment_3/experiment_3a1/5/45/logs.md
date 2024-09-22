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

\section*{Linear Programming Model for Advertising Campaign}

\subsection*{Decision Variables}
Let \( x_a \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost of the advertising campaign:
\[
\text{Minimize } Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\subsection*{Constraints}

\subsubsection*{Click Goals}
The total number of clicks from visitors aged 18-25 must meet the goal:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young}
\]

The total number of clicks from visitors older than 25 must meet the goal:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old}
\]

\subsubsection*{Unique Click Goals}
The total number of unique clicks from visitors aged 18-25 must meet the goal:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_young}
\]

The total number of unique clicks from visitors older than 25 must meet the goal:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_old}
\]

\subsubsection*{Maximum Click Constraints}
The number of clicks purchased for each ad type must not exceed its maximum allowable clicks:
\[
x_a \leq \text{max\_click}_{a} \quad \forall a = 1, 2, \ldots, A
\]

\subsubsection*{Non-negativity Constraints}
The number of clicks cannot be negative:
\[
x_a \geq 0 \quad \forall a = 1, 2, \ldots, A
\]

\subsection*{Summary}
The linear programming model to minimize the total cost for the advertising campaign can be summarized as follows:

\begin{align*}
\text{Minimize } & Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a \\
\text{subject to } & \sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young} \\
& \sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_young} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_old} \\
& x_a \leq \text{max\_click}_{a} \quad \forall a \\
& x_a \geq 0 \quad \forall a
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

\section*{Linear Programming Model for Advertising Campaign}

\subsection*{Decision Variables}
Let \( x_a \) be the number of clicks purchased for ad type \( a \) (in thousands), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Minimize the total cost of the advertising campaign:
\[
\text{Minimize } Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a
\]

\subsection*{Constraints}

\subsubsection*{Click Goals}
The total number of clicks from visitors aged 18-25 must meet the goal:
\[
\sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young}
\]

The total number of clicks from visitors older than 25 must meet the goal:
\[
\sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old}
\]

\subsubsection*{Unique Click Goals}
The total number of unique clicks from visitors aged 18-25 must meet the goal:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_young}
\]

The total number of unique clicks from visitors older than 25 must meet the goal:
\[
\sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_old}
\]

\subsubsection*{Maximum Click Constraints}
The number of clicks purchased for each ad type must not exceed its maximum allowable clicks:
\[
x_a \leq \text{max\_click}_{a} \quad \forall a = 1, 2, \ldots, A
\]

\subsubsection*{Non-negativity Constraints}
The number of clicks cannot be negative:
\[
x_a \geq 0 \quad \forall a = 1, 2, \ldots, A
\]

\subsection*{Summary}
The linear programming model to minimize the total cost for the advertising campaign can be summarized as follows:

\begin{align*}
\text{Minimize } & Z = \sum_{a=1}^{A} \text{cost}_a \cdot x_a \\
\text{subject to } & \sum_{a=1}^{A} \text{young\_click}_{a} \cdot x_a \geq \text{goal\_young} \\
& \sum_{a=1}^{A} \text{old\_click}_{a} \cdot x_a \geq \text{goal\_old} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_young} \\
& \sum_{a=1}^{A} \text{unique\_click}_{a} \cdot x_a \geq \text{goal\_unique\_old} \\
& x_a \leq \text{max\_click}_{a} \quad \forall a \\
& x_a \geq 0 \quad \forall a
\end{align*}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Define the data from the provided JSON format
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

#### Create the LP problem
problem = pulp.LpProblem("Advertising_Campaign", pulp.LpMinimize)

#### Decision variables: number of clicks purchased (in thousands)
x = pulp.LpVariable.dicts("Clicks", range(A), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)), "Total_Cost"

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Goal_Young_Clicks"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Goal_Old_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Goal_Unique_Young_Clicks"
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Goal_Unique_Old_Clicks"

#### Maximum clicks constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_{a+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

