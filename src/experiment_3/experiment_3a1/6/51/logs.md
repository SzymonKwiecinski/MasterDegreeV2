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
Let \( x_a \) be the number of clicks purchased (in thousands) for ad type \( a \), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{align*}
\text{goal\_young} & : \text{Target clicks from visitors aged 18-25 (in thousands)} \\
\text{goal\_old} & : \text{Target clicks from visitors older than 25 (in thousands)} \\
\text{goal\_unique\_young} & : \text{Target unique clicks from visitors aged 18-25 (in thousands)} \\
\text{goal\_unique\_old} & : \text{Target unique clicks from visitors older than 25 (in thousands)} \\
\text{young\_click}_a & : \text{Percentage of clicks from 18-25 age range for ad type } a \\
\text{old\_click}_a & : \text{Percentage of clicks from older visitors for ad type } a \\
\text{cost}_a & : \text{Cost per 1000 clicks for ad type } a \\
\text{max\_click}_a & : \text{Maximum allowable clicks for ad type } a \\
\text{unique\_click}_a & : \text{Estimated percentage of unique visitors for ad type } a \\
\text{budget} & : \text{Total advertising budget}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}
1. **Budget Constraint**:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget}
\]

2. **Click Constraints for Visitors Aged 18-25**:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

3. **Click Constraints for Visitors Older than 25**:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

4. **Unique Clicks for Visitors Aged 18-25**:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

5. **Unique Clicks for Visitors Older than 25**:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_old}
\]

6. **Maximum Click Constraints**:
\[
x_a \leq \text{max\_click}_a \quad \forall a = 1, 2, \ldots, A
\]

7. **Non-negativity Constraints**:
\[
x_a \geq 0 \quad \forall a = 1, 2, \ldots, A
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

\subsection*{Variables}
Let \( x_a \) be the number of clicks purchased (in thousands) for ad type \( a \), where \( a = 1, 2, \ldots, A \).

\subsection*{Parameters}
\begin{align*}
\text{goal\_young} & : \text{Target clicks from visitors aged 18-25 (in thousands)} \\
\text{goal\_old} & : \text{Target clicks from visitors older than 25 (in thousands)} \\
\text{goal\_unique\_young} & : \text{Target unique clicks from visitors aged 18-25 (in thousands)} \\
\text{goal\_unique\_old} & : \text{Target unique clicks from visitors older than 25 (in thousands)} \\
\text{young\_click}_a & : \text{Percentage of clicks from 18-25 age range for ad type } a \\
\text{old\_click}_a & : \text{Percentage of clicks from older visitors for ad type } a \\
\text{cost}_a & : \text{Cost per 1000 clicks for ad type } a \\
\text{max\_click}_a & : \text{Maximum allowable clicks for ad type } a \\
\text{unique\_click}_a & : \text{Estimated percentage of unique visitors for ad type } a \\
\text{budget} & : \text{Total advertising budget}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } Z = \sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a
\]

\subsection*{Constraints}
1. **Budget Constraint**:
\[
\sum_{a=1}^{A} \text{cost}_a \cdot x_a \leq \text{budget}
\]

2. **Click Constraints for Visitors Aged 18-25**:
\[
\sum_{a=1}^{A} \text{young\_click}_a \cdot x_a \geq \text{goal\_young}
\]

3. **Click Constraints for Visitors Older than 25**:
\[
\sum_{a=1}^{A} \text{old\_click}_a \cdot x_a \geq \text{goal\_old}
\]

4. **Unique Clicks for Visitors Aged 18-25**:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_young}
\]

5. **Unique Clicks for Visitors Older than 25**:
\[
\sum_{a=1}^{A} \text{unique\_click}_a \cdot x_a \geq \text{goal\_unique\_old}
\]

6. **Maximum Click Constraints**:
\[
x_a \leq \text{max\_click}_a \quad \forall a = 1, 2, \ldots, A
\]

7. **Non-negativity Constraints**:
\[
x_a \geq 0 \quad \forall a = 1, 2, \ldots, A
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

#### Define the problem
problem = pulp.LpProblem("Custom_Tees_Advertising_Campaign", pulp.LpMaximize)

#### Decision Variables
A = len(data['young_clicks'])  #### Number of ad types
x = pulp.LpVariable.dicts("x", range(1, A + 1), lowBound=0, upBound=None)

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)), "Total_Unique_Clicks"

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a - 1] * x[a] for a in range(1, A + 1)) <= data['budget'], "Budget_Constraint"

#### Click Constraints for Visitors Aged 18-25
problem += pulp.lpSum(data['young_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_young'], "Goal_Young_Constraint"

#### Click Constraints for Visitors Older than 25
problem += pulp.lpSum(data['old_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_old'], "Goal_Old_Constraint"

#### Unique Clicks for Visitors Aged 18-25
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_unique_young'], "Unique_Young_Constraint"

#### Unique Clicks for Visitors Older than 25
problem += pulp.lpSum(data['unique_clicks'][a - 1] * x[a] for a in range(1, A + 1)) >= data['goal_unique_old'], "Unique_Old_Constraint"

#### Maximum Click Constraints
for a in range(1, A + 1):
    problem += x[a] <= data['max_clicks'][a - 1], f"Max_Click_Constraint_{a}"

#### Solve the problem
problem.solve()

#### Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

