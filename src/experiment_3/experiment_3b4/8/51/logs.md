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
To model this problem, we need to formulate it as a Linear Programming (LP) problem. The objective is to maximize the total number of unique clicks given the budget constraint and certain goals for different age groups.

Here's how we can formulate this problem in LaTeX:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Parameters}
\begin{align*}
    & A: \text{Number of ad types} \\
    & \text{goal\_young}: \text{Goal for clicks from 18-25 age group (in thousands)} \\
    & \text{goal\_old}: \text{Goal for clicks from age 25+ group (in thousands)} \\
    & \text{goal\_unique\_young}: \text{Goal for unique clicks from 18-25 age group (in thousands)} \\
    & \text{goal\_unique\_old}: \text{Goal for unique clicks from age 25+ group (in thousands)} \\
    & \text{young\_clicks}_a: \text{Estimated \% of clicks for 18-25 from ad } a \\
    & \text{old\_clicks}_a: \text{Estimated \% of clicks for 25+ from ad } a \\
    & \text{costs}_a: \text{Cost per 1000 clicks for ad } a \\
    & \text{max\_clicks}_a: \text{Maximum allowable clicks for ad } a \text{ (in thousands)} \\
    & \text{unique\_clicks}_a: \text{Estimated \% of unique visitors for ad } a \\
    & \text{budget}: \text{Total advertising budget}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{clicks}_a: \text{Number of clicks purchased for ad type } a \text{ (in thousands)}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize} \quad \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} \left( \text{young\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_young} \\
    & \sum_{a=1}^{A} \left( \text{old\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_old} \\
    & \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_unique\_young} \\
    & \sum_{a=1}^{A} \left( (1 - \text{unique\_clicks}_a) \times \text{clicks}_a \right) \geq \text{goal\_unique\_old} \\
    & \sum_{a=1}^{A} \left( \text{costs}_a \times \text{clicks}_a \right) \leq \text{budget} \\
    & 0 \leq \text{clicks}_a \leq \text{max\_clicks}_a, \quad \forall a = 1, \ldots, A
\end{align*}

\subsection*{Output}
\begin{align*}
    & \text{clicks}: \Big[ \text{clicks}_1, \ldots, \text{clicks}_A \Big] \\
    & \text{total\_unique\_clicks} = \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right)
\end{align*}

\end{document}
```

This LP formulation captures the constraints and objectives of the problem. The objective is to maximize the total number of unique clicks based on predicted percentages for each ad type, while meeting age-specific goals and staying within a budget. The constraints ensure that the required number of clicks from different age groups and budget limitations are respected.

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
\begin{align*}
    & A: \text{Number of ad types} \\
    & \text{goal\_young}: \text{Goal for clicks from 18-25 age group (in thousands)} \\
    & \text{goal\_old}: \text{Goal for clicks from age 25+ group (in thousands)} \\
    & \text{goal\_unique\_young}: \text{Goal for unique clicks from 18-25 age group (in thousands)} \\
    & \text{goal\_unique\_old}: \text{Goal for unique clicks from age 25+ group (in thousands)} \\
    & \text{young\_clicks}_a: \text{Estimated \% of clicks for 18-25 from ad } a \\
    & \text{old\_clicks}_a: \text{Estimated \% of clicks for 25+ from ad } a \\
    & \text{costs}_a: \text{Cost per 1000 clicks for ad } a \\
    & \text{max\_clicks}_a: \text{Maximum allowable clicks for ad } a \text{ (in thousands)} \\
    & \text{unique\_clicks}_a: \text{Estimated \% of unique visitors for ad } a \\
    & \text{budget}: \text{Total advertising budget}
\end{align*}

\subsection*{Decision Variables}
\begin{align*}
    & \text{clicks}_a: \text{Number of clicks purchased for ad type } a \text{ (in thousands)}
\end{align*}

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize} \quad \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right)
\]

\subsection*{Constraints}
\begin{align*}
    & \sum_{a=1}^{A} \left( \text{young\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_young} \\
    & \sum_{a=1}^{A} \left( \text{old\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_old} \\
    & \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right) \geq \text{goal\_unique\_young} \\
    & \sum_{a=1}^{A} \left( (1 - \text{unique\_clicks}_a) \times \text{clicks}_a \right) \geq \text{goal\_unique\_old} \\
    & \sum_{a=1}^{A} \left( \text{costs}_a \times \text{clicks}_a \right) \leq \text{budget} \\
    & 0 \leq \text{clicks}_a \leq \text{max\_clicks}_a, \quad \forall a = 1, \ldots, A
\end{align*}

\subsection*{Output}
\begin{align*}
    & \text{clicks}: \Big[ \text{clicks}_1, \ldots, \text{clicks}_A \Big] \\
    & \text{total\_unique\_clicks} = \sum_{a=1}^{A} \left( \text{unique\_clicks}_a \times \text{clicks}_a \right)
\end{align*}

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

#### Number of ad types
A = len(data['young_clicks'])

#### Problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Decision Variables
clicks = [pulp.LpVariable(f'clicks_{a}', lowBound=0, upBound=data['max_clicks'][a], cat='Continuous') for a in range(A)]

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A))

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_old']
problem += pulp.lpSum(data['unique_clicks'][a] * clicks[a] for a in range(A)) >= data['goal_unique_young']
problem += pulp.lpSum((1 - data['unique_clicks'][a]) * clicks[a] for a in range(A)) >= data['goal_unique_old']
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(A)) <= data['budget']

#### Solve the problem
problem.solve()

#### Outputs
clicks_output = [pulp.value(clicks[a]) for a in range(A)]
total_unique_clicks = pulp.value(problem.objective)

print(f'Clicks: {clicks_output}')
print(f'Total Unique Clicks (Objective Value): <OBJ>{total_unique_clicks}</OBJ>')
```

