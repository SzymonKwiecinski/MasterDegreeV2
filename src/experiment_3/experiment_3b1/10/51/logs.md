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

\subsection*{Parameters}
\begin{itemize}
    \item $A$: Number of different ad types
    \item $goal\_young$: Target clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Target clicks from visitors older than 25 (in thousands)
    \item $goal\_unique\_young$: Target unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Target unique clicks from visitors older than 25 (in thousands)
    \item $young\_click_{a}$: Percentage of clicks from age 18-25 for ad type $a$
    \item $old\_click_{a}$: Percentage of clicks from older visitors for ad type $a$
    \item $cost_{a}$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_{a}$: Maximum allowable clicks for ad type $a$ (in thousands)
    \item $unique\_click_{a}$: Estimated percentage of unique visitors for ad type $a$
    \item $budget$: Total advertising budget
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ (in thousands), for $a = 1, \ldots, A$
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a}
\]

\subsection*{Constraints}
1. Total clicks from age group 18-25:
\[
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} \geq goal\_young
\]

2. Total clicks from age group older than 25:
\[
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} \geq goal\_old
\]

3. Total unique clicks from age group 18-25:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a} \geq goal\_unique\_young
\]

4. Total unique clicks from age group older than 25:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a} \geq goal\_unique\_old
\]

5. Budget constraint:
\[
\sum_{a=1}^{A} cost_{a} \cdot clicks_{a} \leq budget
\]

6. Maximum clicks per ad type:
\[
0 \leq clicks_{a} \leq max\_click_{a}, \quad \forall a \in \{1, \ldots, A\}
\]

\subsection*{Output}
\begin{itemize}
    \item \textbf{Clicks Requested}: $[clicks_{1}, clicks_{2}, \ldots, clicks_{A}]$
    \item \textbf{Total Unique Clicks}: $total\_unique\_clicks$
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
    \item $goal\_young$: Target clicks from visitors aged 18-25 (in thousands)
    \item $goal\_old$: Target clicks from visitors older than 25 (in thousands)
    \item $goal\_unique\_young$: Target unique clicks from visitors aged 18-25 (in thousands)
    \item $goal\_unique\_old$: Target unique clicks from visitors older than 25 (in thousands)
    \item $young\_click_{a}$: Percentage of clicks from age 18-25 for ad type $a$
    \item $old\_click_{a}$: Percentage of clicks from older visitors for ad type $a$
    \item $cost_{a}$: Cost per 1000 clicks for ad type $a$
    \item $max\_click_{a}$: Maximum allowable clicks for ad type $a$ (in thousands)
    \item $unique\_click_{a}$: Estimated percentage of unique visitors for ad type $a$
    \item $budget$: Total advertising budget
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ (in thousands), for $a = 1, \ldots, A$
\end{itemize}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a}
\]

\subsection*{Constraints}
1. Total clicks from age group 18-25:
\[
\sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} \geq goal\_young
\]

2. Total clicks from age group older than 25:
\[
\sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} \geq goal\_old
\]

3. Total unique clicks from age group 18-25:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a} \geq goal\_unique\_young
\]

4. Total unique clicks from age group older than 25:
\[
\sum_{a=1}^{A} unique\_click_{a} \cdot clicks_{a} \geq goal\_unique\_old
\]

5. Budget constraint:
\[
\sum_{a=1}^{A} cost_{a} \cdot clicks_{a} \leq budget
\]

6. Maximum clicks per ad type:
\[
0 \leq clicks_{a} \leq max\_click_{a}, \quad \forall a \in \{1, \ldots, A\}
\]

\subsection*{Output}
\begin{itemize}
    \item \textbf{Clicks Requested}: $[clicks_{1}, clicks_{2}, \ldots, clicks_{A}]$
    \item \textbf{Total Unique Clicks}: $total\_unique\_clicks$
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

#### Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

#### Create the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Decision Variables
A = len(young_clicks)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Print results
clicks_requested = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks Requested: {clicks_requested}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

# START: PY_F 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a python programmer in deep knowledge at Pulp python library and Linear Programming. Python code place between ```python and ```. Fix syntax error in python code which is implementation of matematical model. You receive wrong code between: <WRONG_CODE></WRONG_CODE> You receive error messages between: <CODE_ERROR></CODE_ERROR> Do not change data format! Do not use `while` loop in python code! Do not change code business logic, fix only syntax errors! Print at the end the objective between <OBJ></OBJ> `print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')` 
## START MESSAGE 0 
### ROLE: Role.USER
<WRONG_CODE>
```python
import pulp
import json

#### Load data
data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")

#### Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

#### Create the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Decision Variables
A = len(young_clicks)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Print results
clicks_requested = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks Requested: {clicks_requested}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b1/10/51/python_code0.py", line 5, in <module>
    data = json.loads("{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}")
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/.pyenv/versions/3.11.8/lib/python3.11/json/decoder.py", line 353, in raw_decode
    obj, end = self.scan_once(s, idx)
               ^^^^^^^^^^^^^^^^^^^^^^
json.decoder.JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Load data
data = json.loads('{"goal_young": 500, "goal_old": 600, "goal_unique_young": 250, "goal_unique_old": 300, "young_clicks": [40, 30, 70], "old_clicks": [60, 70, 30], "costs": [75, 100, 120], "max_clicks": [600, 300, 300], "unique_clicks": [40, 75, 90], "budget": 105000}')

#### Parameters
goal_young = data['goal_young']
goal_old = data['goal_old']
goal_unique_young = data['goal_unique_young']
goal_unique_old = data['goal_unique_old']
young_clicks = data['young_clicks']
old_clicks = data['old_clicks']
costs = data['costs']
max_clicks = data['max_clicks']
unique_clicks = data['unique_clicks']
budget = data['budget']

#### Create the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Decision Variables
A = len(young_clicks)
clicks = pulp.LpVariable.dicts("clicks", range(A), lowBound=0, upBound=max_clicks, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
problem += pulp.lpSum(young_clicks[a] * clicks[a] for a in range(A)) >= goal_young, "Young_Clicks_Constraint"
problem += pulp.lpSum(old_clicks[a] * clicks[a] for a in range(A)) >= goal_old, "Old_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_young, "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(unique_clicks[a] * clicks[a] for a in range(A)) >= goal_unique_old, "Unique_Old_Clicks_Constraint"
problem += pulp.lpSum(costs[a] * clicks[a] for a in range(A)) <= budget, "Budget_Constraint"

#### Solve the problem
problem.solve()

#### Print results
clicks_requested = [clicks[a].varValue for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks Requested: {clicks_requested}')
print(f'Total Unique Clicks: {total_unique_clicks}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

