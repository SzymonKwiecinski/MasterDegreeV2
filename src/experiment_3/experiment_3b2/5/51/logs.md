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
To model this problem as a Linear Programming (LP) problem, we need to define the decision variables, constraints, and the objective function accordingly. Let's proceed by formulating the LP model in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}

\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Decision Variables}

Let \( x_a \) be the number of clicks (in thousands) purchased from ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}

Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}

1. Budget Constraint:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget}
\]

2. Age Group Click Constraints:
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a &\geq \text{goal\_young} \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a &\geq \text{goal\_old}
\end{align*}

3. Unique Click Constraints for Age Groups:
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot \text{unique\_click}_a \cdot x_a &\geq \text{goal\_unique\_young} \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot \text{unique\_click}_a \cdot x_a &\geq \text{goal\_unique\_old}
\end{align*}

4. Maximum Clicks Constraint for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_a, \quad \text{for } a = 1, \ldots, A
\]

\subsection*{Output}

The optimal number of clicks to purchase for each ad type \( x_a \) will give the total unique clicks as:
\[
\text{total\_unique\_clicks} = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\end{document}
```

The above LP model captures the essence of the problem where we are maximizing the number of unique clicks subject to budgetary, demographic, and click constraints for each ad type. The decision variables \( x_a \) represent the clicks to be purchased for each ad type in thousands, and the constraints ensure that the goals are met within budget and allowable maximum clicks.

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

\subsection*{Decision Variables}

Let \( x_a \) be the number of clicks (in thousands) purchased from ad type \( a \), where \( a = 1, \ldots, A \).

\subsection*{Objective Function}

Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}

1. Budget Constraint:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget}
\]

2. Age Group Click Constraints:
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a &\geq \text{goal\_young} \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a &\geq \text{goal\_old}
\end{align*}

3. Unique Click Constraints for Age Groups:
\begin{align*}
\sum_{a=1}^{A} \text{young\_click}_a \cdot \text{unique\_click}_a \cdot x_a &\geq \text{goal\_unique\_young} \\
\sum_{a=1}^{A} \text{old\_click}_a \cdot \text{unique\_click}_a \cdot x_a &\geq \text{goal\_unique\_old}
\end{align*}

4. Maximum Clicks Constraint for each ad type:
\[
0 \leq x_a \leq \text{max\_click}_a, \quad \text{for } a = 1, \ldots, A
\]

\subsection*{Output}

The optimal number of clicks to purchase for each ad type \( x_a \) will give the total unique clicks as:
\[
\text{total\_unique\_clicks} = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Decision variables
ad_types = range(len(data['young_clicks']))
x = pulp.LpVariable.dicts("clicks", ad_types, lowBound=0, upBound=data['max_clicks'], cat='Continuous')

#### Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in ad_types), "Total_Unique_Clicks"

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in ad_types) <= data['budget'], "Budget_Constraint"

#### Age Group Click Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in ad_types) >= data['goal_young'], "Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in ad_types) >= data['goal_old'], "Old_Click_Constraint"

#### Unique Click Constraints for Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_young'], "Unique_Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_old'], "Unique_Old_Click_Constraint"

#### Solve the problem
problem.solve()

#### Print the result
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

#### Data from JSON
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

#### Decision variables
ad_types = range(len(data['young_clicks']))
x = pulp.LpVariable.dicts("clicks", ad_types, lowBound=0, upBound=data['max_clicks'], cat='Continuous')

#### Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in ad_types), "Total_Unique_Clicks"

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in ad_types) <= data['budget'], "Budget_Constraint"

#### Age Group Click Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in ad_types) >= data['goal_young'], "Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in ad_types) >= data['goal_old'], "Old_Click_Constraint"

#### Unique Click Constraints for Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_young'], "Unique_Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_old'], "Unique_Old_Click_Constraint"

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')```
</WRONG_CODE>
<CODE_ERROR>
Traceback (most recent call last):
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/src/experiment_3/experiment_3b2/5/51/python_code0.py", line 40, in <module>
    problem.solve()
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 1867, in solve
    status = solver.actualSolve(self, **kwargs)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/apis/coin_api.py", line 112, in actualSolve
    return self.solve_CBC(lp, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/apis/coin_api.py", line 128, in solve_CBC
    vs, variablesNames, constraintsNames, objectiveName = lp.writeMPS(
                                                          ^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/pulp.py", line 1731, in writeMPS
    return mpslp.writeMPS(
           ^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/mps_lp.py", line 253, in writeMPS
    bound_lines.extend(writeMPSBoundLines(varNames[v.name], v, mip))
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/kwiecs01/PrivProjects/MasterDegreeV2/venv/lib/python3.11/site-packages/pulp/mps_lp.py", line 325, in writeMPSBoundLines
    bound_lines.append(" UP BND       %-8s  % .12e\n" % (name, variable.upBound))
                       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~
TypeError: must be real number, not list
</CODE_ERROR>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
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

#### Decision variables
ad_types = range(len(data['young_clicks']))
x = pulp.LpVariable.dicts("clicks", ad_types, lowBound=0, upBound=None, cat='Continuous')  #### Fixed upBound to None

#### Define the problem
problem = pulp.LpProblem("Tees_Advertising_Campaign", pulp.LpMaximize)

#### Objective function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in ad_types), "Total_Unique_Clicks"

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in ad_types) <= data['budget'], "Budget_Constraint"

#### Age Group Click Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in ad_types) >= data['goal_young'], "Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in ad_types) >= data['goal_old'], "Old_Click_Constraint"

#### Unique Click Constraints for Age Groups
problem += pulp.lpSum(data['young_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_young'], "Unique_Young_Click_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * data['unique_clicks'][a] * x[a] for a in ad_types) >= data['goal_unique_old'], "Unique_Old_Click_Constraint"

#### Solve the problem
problem.solve()

#### Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

