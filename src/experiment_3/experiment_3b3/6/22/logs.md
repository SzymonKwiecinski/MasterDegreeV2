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
- The current number of manpower \var{k} is \var{strength_{k}}.
- The company wishes to decide its policy with regard to recruitment, retraining, redundancy and short-time working in the next years.
- There is a natural wastage of labour. 
- A fairly large number of workers leave during their first year. After this, the rate of leaving is much smaller. 
- Taking this into account, the wastage rates of manpower \var{k} with less than one year's service is \var{lessonewaste_{k}}.
- The wastage rates of \var{k} manpower with more than one year's service is \var{moreonewaste_{k}}.
- There has been no recent recruitment and all the workers in the current labour force have been employed for more than one year.
- It is possible to recruit a limited number of workers from outside. 
- In any one year, the maximum number that can be recruited in manpower \var{k} is \var{recruit_{k}}.
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


OBJECTIVE: The company’s declared objective is to minimize redundancy. How should they operate in order to do this?

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

\section*{Manpower Planning Linear Programming Model}

\textbf{Sets:}
\begin{itemize}
    \item $K$: Set of manpower categories.
    \item $I$: Set of years.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirement for category $k$ in year $i$.
    \item $strength_k$: Current number of manpower in category $k$.
    \item $lessonewaste_k$: Wastage rate for manpower in category $k$ with less than one year's service.
    \item $moreonewaste_k$: Wastage rate for manpower in category $k$ with more than one year's service.
    \item $recruit_k$: Maximum number of workers that can be recruited in category $k$.
    \item $costredundancy_k$: Redundancy payment for manpower in category $k$.
    \item $num\_overman$: Maximum number of additional workers that can be employed.
    \item $costoverman_k$: Extra cost per employee per year for overmanning in category $k$.
    \item $num\_shortwork$: Maximum number of workers that can be put on short-time working.
    \item $costshort_k$: Cost per employee per year for short-time working in category $k$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $recruit_{k,i}$: Number of recruits for category $k$ in year $i$.
    \item $overmanning_{k,i}$: Number of overmanned workers in category $k$ in year $i$.
    \item $short_{k,i}$: Number of workers on short-time in category $k$ in year $i$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{k \in K} \sum_{i \in I} (costredundancy_k \cdot \text{Redundancies}_{k,i} + costoverman_k \cdot overmanning_{k,i} + costshort_k \cdot short_{k,i}) 
\end{equation}

\textbf{Constraints:}
\begin{align}
    \text{1. Manpower requirement:} & \quad strength_k(1 - moreonewaste_k) + recruit_{k,i} + overmanning_{k,i} - short_{k,i} \geq requirement_{k,i} \quad \forall k \in K, i \in I \\
    \text{2. Recruitment limit:} & \quad recruit_{k,i} \leq recruit_k \quad \forall k \in K, i \in I \\
    \text{3. Overmanning limit:} & \quad \sum_{k \in K} overmanning_{k,i} \leq num\_overman \quad \forall i \in I \\
    \text{4. Short-time working limit:} & \quad short_{k,i} \leq num\_shortwork \quad \forall k \in K, i \in I \\
    \text{5. Non-negativity:} & \quad recruit_{k,i} \geq 0, \quad overmanning_{k,i} \geq 0, \quad short_{k,i} \geq 0 \quad \forall k \in K, i \in I
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

\section*{Manpower Planning Linear Programming Model}

\textbf{Sets:}
\begin{itemize}
    \item $K$: Set of manpower categories.
    \item $I$: Set of years.
\end{itemize}

\textbf{Parameters:}
\begin{itemize}
    \item $requirement_{k,i}$: Estimated manpower requirement for category $k$ in year $i$.
    \item $strength_k$: Current number of manpower in category $k$.
    \item $lessonewaste_k$: Wastage rate for manpower in category $k$ with less than one year's service.
    \item $moreonewaste_k$: Wastage rate for manpower in category $k$ with more than one year's service.
    \item $recruit_k$: Maximum number of workers that can be recruited in category $k$.
    \item $costredundancy_k$: Redundancy payment for manpower in category $k$.
    \item $num\_overman$: Maximum number of additional workers that can be employed.
    \item $costoverman_k$: Extra cost per employee per year for overmanning in category $k$.
    \item $num\_shortwork$: Maximum number of workers that can be put on short-time working.
    \item $costshort_k$: Cost per employee per year for short-time working in category $k$.
\end{itemize}

\textbf{Decision Variables:}
\begin{itemize}
    \item $recruit_{k,i}$: Number of recruits for category $k$ in year $i$.
    \item $overmanning_{k,i}$: Number of overmanned workers in category $k$ in year $i$.
    \item $short_{k,i}$: Number of workers on short-time in category $k$ in year $i$.
\end{itemize}

\textbf{Objective Function:}
\begin{equation}
\text{Minimize } Z = \sum_{k \in K} \sum_{i \in I} (costredundancy_k \cdot \text{Redundancies}_{k,i} + costoverman_k \cdot overmanning_{k,i} + costshort_k \cdot short_{k,i}) 
\end{equation}

\textbf{Constraints:}
\begin{align}
    \text{1. Manpower requirement:} & \quad strength_k(1 - moreonewaste_k) + recruit_{k,i} + overmanning_{k,i} - short_{k,i} \geq requirement_{k,i} \quad \forall k \in K, i \in I \\
    \text{2. Recruitment limit:} & \quad recruit_{k,i} \leq recruit_k \quad \forall k \in K, i \in I \\
    \text{3. Overmanning limit:} & \quad \sum_{k \in K} overmanning_{k,i} \leq num\_overman \quad \forall i \in I \\
    \text{4. Short-time working limit:} & \quad short_{k,i} \leq num\_shortwork \quad \forall k \in K, i \in I \\
    \text{5. Non-negativity:} & \quad recruit_{k,i} \geq 0, \quad overmanning_{k,i} \geq 0, \quad short_{k,i} \geq 0 \quad \forall k \in K, i \in I
\end{align}

\end{document}</MATH_MODEL>
<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data from JSON
data = {
    'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]],
    'strength': [2000, 1500, 1000],
    'lessonewaste': [0.25, 0.2, 0.1],
    'moreonewaste': [0.1, 0.05, 0.05],
    'recruit': [500, 800, 500],
    'costredundancy': [200, 500, 500],
    'num_overman': 150,
    'costoverman': [1500, 2000, 3000],
    'num_shortwork': 50,
    'costshort': [500, 400, 400]
}

#### Sets
K = range(len(data['strength']))  #### Manpower categories
I = range(len(data['requirement'][0]))  #### Years

#### Problem definition
problem = pulp.LpProblem("Manpower_Planning", pulp.LpMinimize)

#### Decision variables
recruit = pulp.LpVariable.dicts("recruit", (K, I), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", (K, I), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", (K, I), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(data['costredundancy'][k] * (recruit[k][i] - data['requirement'][k][i] + short[k][i] - overmanning[k][i])
                      + data['costoverman'][k] * overmanning[k][i]
                      + data['costshort'][k] * short[k][i]
                      for k in K for i in I)

#### Constraints
for k in K:
    for i in I:
        problem += (
            data['strength'][k] * (1 - data['moreonewaste'][k]) + recruit[k][i] + overmanning[k][i] - short[k][i]
            >= data['requirement'][k][i], f"ManpowerRequirement_{k}_{i}"
        )
        problem += recruit[k][i] <= data['recruit'][k], f"RecruitmentLimit_{k}_{i}"
        problem += short[k][i] <= data['num_shortwork'], f"ShortTimeWorkingLimit_{k}_{i}"

for i in I:
    problem += (
        pulp.lpSum(overmanning[k][i] for k in K) <= data['num_overman'], f"OvermanningLimit_{i}"
    )

#### Solve the problem
problem.solve()

#### Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

