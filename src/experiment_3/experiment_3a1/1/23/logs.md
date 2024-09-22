# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP
PROBLEM INFO:

- A company is undergoing a number of changes that will affect its manpower requirements in future years. 
- Owing to the installation of new machinery, fewer unskilled but more skilled and semi-skilled workers will be required. 
- In addition to this, a downturn in trade is expected in the next year, which will reduce the need for workers in all categories.
- The estimated manpower requirements for manpower \var{k} in year \var{i} is \var{requirement_{k, i}}.
- The current strength of manpower \var{k} is \var{strength_{k}}.
- The company wishes to decide its policy with regard to recruitment, retraining, redundancy and short-time working in the next years.
- There is a natural wastage of labour. 
- A fairly large number of workers leave during their first year. After this, the rate is much smaller. 
- Taking this into account, the wastage rates of \var{k} manpower with less than one year's service is \var{lessonewaste_{k}}.
- The wastage rates of \var{k} manpower with more than one year's service is \var{moreonewaste_{k}}.
- There has been no recent recruitment and all workers in the current labour force have been employed for more than one year.
- It is possible to recruit a limited number of workers from outside. 
- In any one year, the numbers that can be recruited in manpower \var{k} is \var{recruit_{k}}.
- The redundancy payment to manpower \var{k} is \var{costredundancy_{k}}.
- It is possible to employ up to \var{num_overman} more workers over the whole company than are needed, but the extra costs per employee per year is \var{costoverman_{k}} for manpower \var{k}.
- Up to \var{num_shortwork} workers in each category of skill can be put on short-time working. 
- The cost of this (per employee per year) is \var{costshort_{k}} for manpower \var{k}.
- An employee on short-time working meets the production requirements of half a full-time employee.


INPUT FORMAT:

{
    "requirement": [[requirement_{k, i} for i in 1,...,I] for k in 1,...,K],
    "strength": [strength_{k} for k in 1,...,K],
    "lessonewaste": [lessonewaste_{k} for k in 1,...,K],
    "moreonewaste": [lessonewaste_{k} for k in 1,...,K],
    "recruit": [recruit_{k} for k in 1,...,K],
    "costredundancy": [costredundancy_{k} for k in 1,...,K],
    "num_overman": num_overman,
    "costoverman": [costoverman_{k} for k in 1,...,K],
    "num_shortwork": num_shortwork
    "costshort": [costshort_{k} for k in 1,...,K],
}


OBJECTIVE: The company’s declared objective is to minimize costs. How should they operate in order to do this?

OUTPUT INFO:

- \var{recruit} represents the number of each recruit manpower to employ each year
- \var{overmanning} represents the number of each overmanning manpower to employ each year
- \var{short} represents the number of each short-time manpower to employ each year

OUTPUT FORMAT:

{
    "recruit": [[recruit_{k, i} for i in 1,...,I] for k in 1,...,K],
    "overmanning": [[overmanning_{k, i} for i in 1,...,I] for k in 1,...,K],
    "short": [[short_{k, i} for i in 1,...,I] for k in 1,...,K]
}
</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Mathematical Model for Workforce Management}

\textbf{Indices:} \\
\begin{itemize}
    \item $k$: Index for manpower categories, where $k = 1, 2, \ldots, K$ 
    \item $i$: Index for years, where $i = 1, 2, \ldots, I$
\end{itemize}

\textbf{Parameters:} \\
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirement for category $k$ in year $i$
    \item $strength_k$: Current strength of manpower for category $k$
    \item $lessonewaste_k$: Wastage rate of manpower with less than one year's service for category $k$
    \item $moreonewaste_k$: Wastage rate of manpower with more than one year's service for category $k$
    \item $recruit_k$: Maximum number of recruits possible for category $k$
    \item $costredundancy_k$: Cost of redundancy payment for manpower category $k$
    \item $num\_overman$: Maximum number of overmanning allowed across the company
    \item $costoverman_k$: Cost per employee per year for overmanning in category $k$
    \item $num\_shortwork$: Maximum number of short-time workers allowed in each category
    \item $costshort_k$: Cost per employee per year for short-time working in category $k$
\end{itemize}

\textbf{Decision Variables:} \\
\begin{itemize}
    \item $recruit_{k,i}$: Number of recruits of manpower category $k$ in year $i$
    \item $overmanning_{k,i}$: Number of overmanned employees of category $k$ in year $i$
    \item $short_{k,i}$: Number of short-time employees of category $k$ in year $i$
\end{itemize}

\textbf{Objective Function:} \\
Minimize total costs:
\[
\text{Minimize} \; Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( costredundancy_k \cdot (strength_k - requirement_{k,i})^+ + costoverman_k \cdot overmanning_{k,i} + costshort_k \cdot short_{k,i} \right)
\]

\textbf{Constraints:} \\
1. Manpower requirement constraint:
\[
strength_k - (1 - lessonewaste_k) \cdot (strength_k - \sum_{i=1}^{I} recruit_{k,i}) + overmanning_{k,i} + \frac{short_{k,i}}{2} \geq requirement_{k,i}, \quad \forall k, i
\]

2. Recruitment constraint:
\[
recruit_{k,i} \leq recruit_k, \quad \forall k, i
\]

3. Overmanning constraint:
\[
\sum_{k=1}^{K} overmanning_{k,i} \leq num\_overman, \quad \forall i
\]

4. Short-time working constraint:
\[
short_{k,i} \leq num\_shortwork, \quad \forall k, i
\]

5. Non-negativity constraints:
\[
recruit_{k,i} \geq 0, \; overmanning_{k,i} \geq 0, \; short_{k,i} \geq 0, \quad \forall k, i
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

\section*{Mathematical Model for Workforce Management}

\textbf{Indices:} \\
\begin{itemize}
    \item $k$: Index for manpower categories, where $k = 1, 2, \ldots, K$ 
    \item $i$: Index for years, where $i = 1, 2, \ldots, I$
\end{itemize}

\textbf{Parameters:} \\
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirement for category $k$ in year $i$
    \item $strength_k$: Current strength of manpower for category $k$
    \item $lessonewaste_k$: Wastage rate of manpower with less than one year's service for category $k$
    \item $moreonewaste_k$: Wastage rate of manpower with more than one year's service for category $k$
    \item $recruit_k$: Maximum number of recruits possible for category $k$
    \item $costredundancy_k$: Cost of redundancy payment for manpower category $k$
    \item $num\_overman$: Maximum number of overmanning allowed across the company
    \item $costoverman_k$: Cost per employee per year for overmanning in category $k$
    \item $num\_shortwork$: Maximum number of short-time workers allowed in each category
    \item $costshort_k$: Cost per employee per year for short-time working in category $k$
\end{itemize}

\textbf{Decision Variables:} \\
\begin{itemize}
    \item $recruit_{k,i}$: Number of recruits of manpower category $k$ in year $i$
    \item $overmanning_{k,i}$: Number of overmanned employees of category $k$ in year $i$
    \item $short_{k,i}$: Number of short-time employees of category $k$ in year $i$
\end{itemize}

\textbf{Objective Function:} \\
Minimize total costs:
\[
\text{Minimize} \; Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( costredundancy_k \cdot (strength_k - requirement_{k,i})^+ + costoverman_k \cdot overmanning_{k,i} + costshort_k \cdot short_{k,i} \right)
\]

\textbf{Constraints:} \\
1. Manpower requirement constraint:
\[
strength_k - (1 - lessonewaste_k) \cdot (strength_k - \sum_{i=1}^{I} recruit_{k,i}) + overmanning_{k,i} + \frac{short_{k,i}}{2} \geq requirement_{k,i}, \quad \forall k, i
\]

2. Recruitment constraint:
\[
recruit_{k,i} \leq recruit_k, \quad \forall k, i
\]

3. Overmanning constraint:
\[
\sum_{k=1}^{K} overmanning_{k,i} \leq num\_overman, \quad \forall i
\]

4. Short-time working constraint:
\[
short_{k,i} \leq num\_shortwork, \quad \forall k, i
\]

5. Non-negativity constraints:
\[
recruit_{k,i} \geq 0, \; overmanning_{k,i} \geq 0, \; short_{k,i} \geq 0, \quad \forall k, i
\]

\end{document}</MATH_MODEL>
<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Sample data in json format
data = json.loads('''
{
    "requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 
    "strength": [2000, 1500, 1000], 
    "lessonewaste": [0.25, 0.2, 0.1], 
    "moreonewaste": [0.1, 0.05, 0.05], 
    "recruit": [500, 800, 500], 
    "costredundancy": [200, 500, 500], 
    "num_overman": 150, 
    "costoverman": [1500, 2000, 3000], 
    "num_shortwork": 50, 
    "costshort": [500, 400, 400]
}
''')

#### Extracting data
K = len(data['strength'])  #### Number of manpower categories
I = len(data['requirement'])  #### Number of years
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit_limit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

#### Create the linear programming problem
problem = pulp.LpProblem("Workforce_Management", pulp.LpMinimize)

#### Decision Variables
recruit = pulp.LpVariable.dicts("recruit", (range(K), range(I)), lowBound=0, cat='Integer')
overmanning = pulp.LpVariable.dicts("overmanning", (range(K), range(I)), lowBound=0, cat='Integer')
short = pulp.LpVariable.dicts("short", (range(K), range(I)), lowBound=0, cat='Integer')

#### Objective Function
problem += pulp.lpSum(
    [costredundancy[k] * max(0, strength[k] - requirement[i][k]) + 
     costoverman[k] * overmanning[k][i] + 
     costshort[k] * short[k][i]
     for k in range(K) for i in range(I)]
)

#### Constraints
#### Manpower requirement constraint
for i in range(I):
    for k in range(K):
        problem += (strength[k] - (1 - lessonewaste[k]) * (strength[k] - pulp.lpSum(recruit[k][j] for j in range(I))) +
                     overmanning[k][i] + short[k][i] / 2 >= requirement[i][k])

#### Recruitment constraint
for i in range(I):
    for k in range(K):
        problem += (recruit[k][i] <= recruit_limit[k])

#### Overmanning constraint
for i in range(I):
    problem += (pulp.lpSum(overmanning[k][i] for k in range(K)) <= num_overman)

#### Short-time working constraint
for i in range(I):
    for k in range(K):
        problem += (short[k][i] <= num_shortwork)

#### Solve the problem
problem.solve()

#### Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

