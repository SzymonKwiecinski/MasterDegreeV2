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
To model this problem, we need to use linear programming. The goal is to maximize the number of unique clicks, while considering constraints related to budget, targeted demographics, and maximum allowable clicks for each ad type. Here's how you can formulate this problem using LaTeX and linear programming notation:

```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Custom Tees Advertising Campaign}

\subsection*{Decision Variables}
Let \( x_a \) represent the number of thousands of clicks purchased for ad type \( a \), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } \sum_{a=1}^{A} \left( \text{unique\_click}_a \times x_a \right)
\]

\subsection*{Constraints}

1. \textbf{Budget Constraint:}
   \[
   \sum_{a=1}^{A} \left( \text{cost}_a \times x_a \right) \leq \text{budget}
   \]

2. \textbf{Age Group Clicks Constraints:}
   - For visitors aged 18-25:
   \[
   \sum_{a=1}^{A} \left( \text{young\_click}_a \times x_a \right) \geq \text{goal\_young}
   \]

   - For visitors older than 25:
   \[
   \sum_{a=1}^{A} \left( \text{old\_click}_a \times x_a \right) \geq \text{goal\_old}
   \]

3. \textbf{Unique Clicks Constraints:}
   - For visitors aged 18-25:
   \[
   \sum_{a=1}^{A} \left( \text{unique\_click}_a \times \text{young\_click}_a \times x_a \right) \geq \text{goal\_unique\_young}
   \]

   - For visitors older than 25:
   \[
   \sum_{a=1}^{A} \left( \text{unique\_click}_a \times \text{old\_click}_a \times x_a \right) \geq \text{goal\_unique\_old}
   \]

4. \textbf{Maximum Clicks Constraint:}
   \[
   x_a \leq \text{max\_click}_a, \quad \forall a = 1, 2, \ldots, A
   \]

5. \textbf{Non-negativity Constraint:}
   \[
   x_a \geq 0, \quad \forall a = 1, 2, \ldots, A
   \]

\end{document}
```

This model maximizes the weighted sum of unique clicks, subject to constraints on budget, demographic targeting, and the allowable number of clicks for each ad type. The variables are controlled by both demographic and budgetary constraints, ensuring the solution is feasible and optimal relative to the given inputs.

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
Let \( x_a \) represent the number of thousands of clicks purchased for ad type \( a \), where \( a = 1, 2, \ldots, A \).

\subsection*{Objective Function}
Maximize the total number of unique clicks:
\[
\text{Maximize } \sum_{a=1}^{A} \left( \text{unique\_click}_a \times x_a \right)
\]

\subsection*{Constraints}

1. \textbf{Budget Constraint:}
   \[
   \sum_{a=1}^{A} \left( \text{cost}_a \times x_a \right) \leq \text{budget}
   \]

2. \textbf{Age Group Clicks Constraints:}
   - For visitors aged 18-25:
   \[
   \sum_{a=1}^{A} \left( \text{young\_click}_a \times x_a \right) \geq \text{goal\_young}
   \]

   - For visitors older than 25:
   \[
   \sum_{a=1}^{A} \left( \text{old\_click}_a \times x_a \right) \geq \text{goal\_old}
   \]

3. \textbf{Unique Clicks Constraints:}
   - For visitors aged 18-25:
   \[
   \sum_{a=1}^{A} \left( \text{unique\_click}_a \times \text{young\_click}_a \times x_a \right) \geq \text{goal\_unique\_young}
   \]

   - For visitors older than 25:
   \[
   \sum_{a=1}^{A} \left( \text{unique\_click}_a \times \text{old\_click}_a \times x_a \right) \geq \text{goal\_unique\_old}
   \]

4. \textbf{Maximum Clicks Constraint:}
   \[
   x_a \leq \text{max\_click}_a, \quad \forall a = 1, 2, \ldots, A
   \]

5. \textbf{Non-negativity Constraint:}
   \[
   x_a \geq 0, \quad \forall a = 1, 2, \ldots, A
   \]

\end{document}</MATH_MODEL>
<DATA>
{'goal_young': 500, 'goal_old': 600, 'goal_unique_young': 250, 'goal_unique_old': 300, 'young_clicks': [40, 30, 70], 'old_clicks': [60, 70, 30], 'costs': [75, 100, 120], 'max_clicks': [600, 300, 300], 'unique_clicks': [40, 75, 90], 'budget': 105000}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data provided in JSON format
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
A = len(data['costs'])

#### Create the problem
problem = pulp.LpProblem("Maximize_Unique_Clicks", pulp.LpMaximize)

#### Decision Variables
x = pulp.LpVariable.dicts("x", range(A), lowBound=0, upBound=None)

#### Objective Function
problem += pulp.lpSum(data['unique_clicks'][a] * x[a] for a in range(A)), "Total_Unique_Clicks"

#### Constraints
#### Budget Constraint
problem += pulp.lpSum(data['costs'][a] * x[a] for a in range(A)) <= data['budget'], "Budget_Constraint"

#### Age Group Clicks Constraints
problem += pulp.lpSum(data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_young'], "Young_Clicks_Constraint"
problem += pulp.lpSum(data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_old'], "Old_Clicks_Constraint"

#### Unique Clicks Constraints
problem += pulp.lpSum(data['unique_clicks'][a] * data['young_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_young'], "Unique_Young_Clicks_Constraint"
problem += pulp.lpSum(data['unique_clicks'][a] * data['old_clicks'][a] * x[a] for a in range(A)) >= data['goal_unique_old'], "Unique_Old_Clicks_Constraint"

#### Maximum Clicks Constraints
for a in range(A):
    problem += x[a] <= data['max_clicks'][a], f"Max_Clicks_Constraint_{a+1}"

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

