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

\section*{Linear Programming Model for Manpower Management}

\subsection*{Sets}
\begin{itemize}
    \item $K$: Set of manpower categories (e.g., skilled, semi-skilled, unskilled).
    \item $I$: Set of future years.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirements for category $k$ in year $i$.
    \item $strength_{k}$: Current strength of manpower in category $k$.
    \item $lessonewaste_{k}$: Wastage rate of category $k$ manpower with less than one year's service.
    \item $moreonewaste_{k}$: Wastage rate of category $k$ manpower with more than one year's service.
    \item $recruit_{k}$: Maximum number of workers that can be recruited for category $k$.
    \item $costredundancy_{k}$: Redundancy payment for category $k$ manpower.
    \item $num\_overman$: Maximum number of overmanned workers across the company.
    \item $costoverman_{k}$: Extra cost per employee per year for overmanning category $k$.
    \item $num\_shortwork$: Maximum number of workers in each category that can be put on short-time working.
    \item $costshort_{k}$: Cost per employee per year for short-time working of category $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $recruit_{k,i}$: Number of workers recruited for category $k$ in year $i$.
    \item $overmanning_{k,i}$: Number of overmanned workers for category $k$ in year $i$.
    \item $short_{k,i}$: Number of workers on short-time working for category $k$ in year $i$.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{k \in K} \sum_{i \in I} \left( costredundancy_{k} \cdot redundancy_{k,i} + costoverman_{k} \cdot overmanning_{k,i} + costshort_{k} \cdot short_{k,i} \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{Current manpower for each category in year } i: \\
    strength_{k} - \sum_{j=1}^{i} \left( lessonewaste_{k} \cdot recruit_{k,j} + moreonewaste_{k} \cdot strength_{k} \right) + recruit_{k,i} + overmanning_{k,i} - short_{k,i} & = requirement_{k,i} \quad \forall k \in K, \forall i \in I \\
    \text{Wastage for less than one year: } \\
    \sum_{j=1}^{i-1} recruit_{k,j} \cdot lessonewaste_{k} & \leq strength_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Wastage for more than one year: } \\
    \sum_{j=1}^{i-1} (strength_{k} \cdot moreonewaste_{k}) & \leq strength_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Recruitment limits: } \\
    recruit_{k,i} & \leq recruit_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Overmanning limits: } \\
    \sum_{i=1}^{I} overmanning_{k,i} & \leq num\_overman \quad \forall k \in K \\
    \text{Short-time working limits: } \\
    short_{k,i} & \leq num\_shortwork \quad \forall k \in K, \forall i \in I \\
    \text{Non-negativity: } \\
    recruit_{k,i}, overmanning_{k,i}, short_{k,i} & \geq 0 \quad \forall k \in K, \forall i \in I 
\end{align}

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

\section*{Linear Programming Model for Manpower Management}

\subsection*{Sets}
\begin{itemize}
    \item $K$: Set of manpower categories (e.g., skilled, semi-skilled, unskilled).
    \item $I$: Set of future years.
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirements for category $k$ in year $i$.
    \item $strength_{k}$: Current strength of manpower in category $k$.
    \item $lessonewaste_{k}$: Wastage rate of category $k$ manpower with less than one year's service.
    \item $moreonewaste_{k}$: Wastage rate of category $k$ manpower with more than one year's service.
    \item $recruit_{k}$: Maximum number of workers that can be recruited for category $k$.
    \item $costredundancy_{k}$: Redundancy payment for category $k$ manpower.
    \item $num\_overman$: Maximum number of overmanned workers across the company.
    \item $costoverman_{k}$: Extra cost per employee per year for overmanning category $k$.
    \item $num\_shortwork$: Maximum number of workers in each category that can be put on short-time working.
    \item $costshort_{k}$: Cost per employee per year for short-time working of category $k$.
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item $recruit_{k,i}$: Number of workers recruited for category $k$ in year $i$.
    \item $overmanning_{k,i}$: Number of overmanned workers for category $k$ in year $i$.
    \item $short_{k,i}$: Number of workers on short-time working for category $k$ in year $i$.
\end{itemize}

\subsection*{Objective Function}
The objective is to minimize the total cost:
\[
\text{Minimize } Z = \sum_{k \in K} \sum_{i \in I} \left( costredundancy_{k} \cdot redundancy_{k,i} + costoverman_{k} \cdot overmanning_{k,i} + costshort_{k} \cdot short_{k,i} \right)
\]

\subsection*{Constraints}
\begin{align}
    \text{Current manpower for each category in year } i: \\
    strength_{k} - \sum_{j=1}^{i} \left( lessonewaste_{k} \cdot recruit_{k,j} + moreonewaste_{k} \cdot strength_{k} \right) + recruit_{k,i} + overmanning_{k,i} - short_{k,i} & = requirement_{k,i} \quad \forall k \in K, \forall i \in I \\
    \text{Wastage for less than one year: } \\
    \sum_{j=1}^{i-1} recruit_{k,j} \cdot lessonewaste_{k} & \leq strength_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Wastage for more than one year: } \\
    \sum_{j=1}^{i-1} (strength_{k} \cdot moreonewaste_{k}) & \leq strength_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Recruitment limits: } \\
    recruit_{k,i} & \leq recruit_{k} \quad \forall k \in K, \forall i \in I \\
    \text{Overmanning limits: } \\
    \sum_{i=1}^{I} overmanning_{k,i} & \leq num\_overman \quad \forall k \in K \\
    \text{Short-time working limits: } \\
    short_{k,i} & \leq num\_shortwork \quad \forall k \in K, \forall i \in I \\
    \text{Non-negativity: } \\
    recruit_{k,i}, overmanning_{k,i}, short_{k,i} & \geq 0 \quad \forall k \in K, \forall i \in I 
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp
import json

#### Data from JSON
data = json.loads('{"requirement": [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], "strength": [2000, 1500, 1000], "lessonewaste": [0.25, 0.2, 0.1], "moreonewaste": [0.1, 0.05, 0.05], "recruit": [500, 800, 500], "costredundancy": [200, 500, 500], "num_overman": 150, "costoverman": [1500, 2000, 3000], "num_shortwork": 50, "costshort": [500, 400, 400]}')

#### Extracting data
requirement = data['requirement']
strength = data['strength']
lessonewaste = data['lessonewaste']
moreonewaste = data['moreonewaste']
recruit = data['recruit']
costredundancy = data['costredundancy']
num_overman = data['num_overman']
costoverman = data['costoverman']
num_shortwork = data['num_shortwork']
costshort = data['costshort']

K = range(len(strength))
I = range(len(requirement[0]))

#### Create the problem
problem = pulp.LpProblem("ManpowerManagement", pulp.LpMinimize)

#### Decision Variables
recruit_vars = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0)
overmanning_vars = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0)
short_vars = pulp.LpVariable.dicts("short", (K, I), lowBound=0)

#### Objective Function
problem += pulp.lpSum(costredundancy[k] * recruit_vars[k][i] + 
                      costoverman[k] * overmanning_vars[k][i] + 
                      costshort[k] * short_vars[k][i] 
                      for k in K for i in I)

#### Constraints
for k in K:
    for i in I:
        #### Current manpower
        problem += (strength[k] - 
                     pulp.lpSum(lessonewaste[k] * recruit_vars[k][j] for j in range(i + 1)) - 
                     moreonewaste[k] * strength[k] * (i + 1) + 
                     recruit_vars[k][i] + 
                     overmanning_vars[k][i] - 
                     short_vars[k][i] == requirement[k][i])

#### Wastage for less than one year
for k in K:
    for i in I:
        if i > 0:
            problem += pulp.lpSum(recruit_vars[k][j] * lessonewaste[k] for j in range(i)) <= strength[k]

#### Wastage for more than one year
for k in K:
    for i in I:
        if i > 0:
            problem += pulp.lpSum(strength[k] * moreonewaste[k] for j in range(i)) <= strength[k]

#### Recruitment limits
for k in K:
    for i in I:
        problem += recruit_vars[k][i] <= recruit[k]

#### Overmanning limits
for k in K:
    problem += pulp.lpSum(overmanning_vars[k][i] for i in I) <= num_overman

#### Short-time working limits
for k in K:
    for i in I:
        problem += short_vars[k][i] <= num_shortwork

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

