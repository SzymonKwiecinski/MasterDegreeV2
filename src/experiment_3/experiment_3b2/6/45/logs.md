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
To solve this problem, we'll formulate a linear programming model to minimize the total cost of the advertising campaign while satisfying the constraints for the number of clicks from different age groups and unique visitors. Here is the mathematical model in LaTeX format:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\textbf{Decision Variables:}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ in thousands, for $a = 1, \ldots, A$.
\end{itemize}

\textbf{Objective:}
Minimize the total cost of the ad campaign:
\[
\text{Minimize } \sum_{a=1}^{A} cost_{a} \cdot clicks_{a}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total clicks from visitors aged 18-25:
    \[
    \sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} \geq goal\_young
    \]
    
    \item Total clicks from older visitors:
    \[
    \sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} \geq goal\_old
    \]
    
    \item Total unique clicks from visitors aged 18-25:
    \[
    \sum_{a=1}^{A} unique\_click_{a} \cdot young\_click_{a} \cdot clicks_{a} \geq goal\_unique\_young
    \]
    
    \item Total unique clicks from older visitors:
    \[
    \sum_{a=1}^{A} unique\_click_{a} \cdot old\_click_{a} \cdot clicks_{a} \geq goal\_unique\_old
    \]
    
    \item Maximum allowable clicks for each ad type:
    \[
    0 \leq clicks_{a} \leq max\_click_{a}, \quad \forall a = 1, \ldots, A
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $\{clicks_{a}\}_{a=1}^{A}$: Number of clicks purchased for each ad type.
    \item $total\_cost$: Total cost of the ad campaign.
\end{itemize}

\end{document}
```

This model entails minimizing the cost function subject to constraints for achieving the required number of clicks from different age demographics, both total and unique, while respecting the maximum allowed clicks for each ad type. The decision variables represent the number of thousands of clicks purchased for each ad type.

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

\textbf{Decision Variables:}
\begin{itemize}
    \item $clicks_{a}$: Number of clicks purchased for ad type $a$ in thousands, for $a = 1, \ldots, A$.
\end{itemize}

\textbf{Objective:}
Minimize the total cost of the ad campaign:
\[
\text{Minimize } \sum_{a=1}^{A} cost_{a} \cdot clicks_{a}
\]

\textbf{Constraints:}
\begin{itemize}
    \item Total clicks from visitors aged 18-25:
    \[
    \sum_{a=1}^{A} young\_click_{a} \cdot clicks_{a} \geq goal\_young
    \]
    
    \item Total clicks from older visitors:
    \[
    \sum_{a=1}^{A} old\_click_{a} \cdot clicks_{a} \geq goal\_old
    \]
    
    \item Total unique clicks from visitors aged 18-25:
    \[
    \sum_{a=1}^{A} unique\_click_{a} \cdot young\_click_{a} \cdot clicks_{a} \geq goal\_unique\_young
    \]
    
    \item Total unique clicks from older visitors:
    \[
    \sum_{a=1}^{A} unique\_click_{a} \cdot old\_click_{a} \cdot clicks_{a} \geq goal\_unique\_old
    \]
    
    \item Maximum allowable clicks for each ad type:
    \[
    0 \leq clicks_{a} \leq max\_click_{a}, \quad \forall a = 1, \ldots, A
    \]
\end{itemize}

\textbf{Output:}
\begin{itemize}
    \item $\{clicks_{a}\}_{a=1}^{A}$: Number of clicks purchased for each ad type.
    \item $total\_cost$: Total cost of the ad campaign.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from the JSON format
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

#### Define the problem
problem = pulp.LpProblem("Custom_Tees_Ad_Campaign", pulp.LpMinimize)

#### Decision variables
number_of_ads = len(data['costs'])
clicks = pulp.LpVariable.dicts("clicks", range(number_of_ads), lowBound=0)

#### Objective function
problem += pulp.lpSum(data['costs'][a] * clicks[a] for a in range(number_of_ads))

#### Constraints
problem += pulp.lpSum(data['young_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_young']
problem += pulp.lpSum(data['old_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_old']
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_unique_young']
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * clicks[a] for a in range(number_of_ads)) >= data['goal_unique_old']

#### Maximum clicks constraint
for a in range(number_of_ads):
    problem += clicks[a] <= data['max_clicks'][a]

#### Solve the problem
problem.solve()

#### Output the results
results = {a: clicks[a].varValue for a in range(number_of_ads)}
total_cost = pulp.value(problem.objective)

print(f'Clicks: {results}')
print(f'Total Cost: {total_cost}')

print(f' (Objective Value): <OBJ>{total_cost}</OBJ>')
```

