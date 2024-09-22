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

\section*{Linear Programming Model for Manpower Optimization}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for manpower categories, \( k = 1, 2, \ldots, K \)
    \item \( i \): Index for years, \( i = 1, 2, \ldots, I \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{requirement}_{k, i} \): Estimated manpower requirements for category \( k \) in year \( i \)
    \item \( \text{strength}_{k} \): Current strength of manpower category \( k \)
    \item \( \text{lessonewaste}_{k} \): Wastage rate of manpower category \( k \) with less than one year's service
    \item \( \text{moreonewaste}_{k} \): Wastage rate of manpower category \( k \) with more than one year's service
    \item \( \text{recruit}_{k} \): Limit on the number of recruits for category \( k \)
    \item \( \text{costredundancy}_{k} \): Redundancy payment for manpower category \( k \)
    \item \( \text{num\_overman} \): Maximum number of overmanned workers allowed
    \item \( \text{costoverman}_{k} \): Extra cost per employee for overmanning in category \( k \)
    \item \( \text{num\_shortwork} \): Maximum number of workers allowed on short-time working per category
    \item \( \text{costshort}_{k} \): Cost per employee per year for short-time working in category \( k \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{recruit}_{k, i} \): Number of recruits for manpower category \( k \) in year \( i \)
    \item \( \text{overmanning}_{k, i} \): Number of overmanned workers for manpower category \( k \) in year \( i \)
    \item \( \text{short}_{k, i} \): Number of workers on short-time working for manpower category \( k \) in year \( i \)
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Minimize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{costredundancy}_{k} \cdot \text{recruit}_{k, i} + \text{costoverman}_{k} \cdot \text{overmanning}_{k, i} + \text{costshort}_{k} \cdot \text{short}_{k, i} \right)
\]

\subsection*{Constraints}
1. Manpower requirements:
\[
\text{strength}_{k} - \text{lessonewaste}_{k} \cdot \text{recruit}_{k, i} - \text{moreonewaste}_{k} \cdot \text{strength}_{k} + \text{recruit}_{k, i} + \text{short}_{k, i} + \text{overmanning}_{k, i} \geq \text{requirement}_{k, i}, \quad \forall k, i
\]

2. Recruitment limits:
\[
\text{recruit}_{k, i} \leq \text{recruit}_{k}, \quad \forall k, i
\]

3. Overmanning limits:
\[
\sum_{k=1}^{K} \text{overmanning}_{k, i} \leq \text{num\_overman}, \quad \forall i
\]

4. Short-time working limits:
\[
\text{short}_{k, i} \leq \text{num\_shortwork}, \quad \forall k, i
\]

5. Non-negativity constraints:
\[
\text{recruit}_{k, i}, \text{overmanning}_{k, i}, \text{short}_{k, i} \geq 0, \quad \forall k, i
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

\section*{Linear Programming Model for Manpower Optimization}

\subsection*{Indices}
\begin{itemize}
    \item \( k \): Index for manpower categories, \( k = 1, 2, \ldots, K \)
    \item \( i \): Index for years, \( i = 1, 2, \ldots, I \)
\end{itemize}

\subsection*{Parameters}
\begin{itemize}
    \item \( \text{requirement}_{k, i} \): Estimated manpower requirements for category \( k \) in year \( i \)
    \item \( \text{strength}_{k} \): Current strength of manpower category \( k \)
    \item \( \text{lessonewaste}_{k} \): Wastage rate of manpower category \( k \) with less than one year's service
    \item \( \text{moreonewaste}_{k} \): Wastage rate of manpower category \( k \) with more than one year's service
    \item \( \text{recruit}_{k} \): Limit on the number of recruits for category \( k \)
    \item \( \text{costredundancy}_{k} \): Redundancy payment for manpower category \( k \)
    \item \( \text{num\_overman} \): Maximum number of overmanned workers allowed
    \item \( \text{costoverman}_{k} \): Extra cost per employee for overmanning in category \( k \)
    \item \( \text{num\_shortwork} \): Maximum number of workers allowed on short-time working per category
    \item \( \text{costshort}_{k} \): Cost per employee per year for short-time working in category \( k \)
\end{itemize}

\subsection*{Decision Variables}
\begin{itemize}
    \item \( \text{recruit}_{k, i} \): Number of recruits for manpower category \( k \) in year \( i \)
    \item \( \text{overmanning}_{k, i} \): Number of overmanned workers for manpower category \( k \) in year \( i \)
    \item \( \text{short}_{k, i} \): Number of workers on short-time working for manpower category \( k \) in year \( i \)
\end{itemize}

\subsection*{Objective Function}
Minimize total cost:
\[
\text{Minimize } Z = \sum_{i=1}^{I} \sum_{k=1}^{K} \left( \text{costredundancy}_{k} \cdot \text{recruit}_{k, i} + \text{costoverman}_{k} \cdot \text{overmanning}_{k, i} + \text{costshort}_{k} \cdot \text{short}_{k, i} \right)
\]

\subsection*{Constraints}
1. Manpower requirements:
\[
\text{strength}_{k} - \text{lessonewaste}_{k} \cdot \text{recruit}_{k, i} - \text{moreonewaste}_{k} \cdot \text{strength}_{k} + \text{recruit}_{k, i} + \text{short}_{k, i} + \text{overmanning}_{k, i} \geq \text{requirement}_{k, i}, \quad \forall k, i
\]

2. Recruitment limits:
\[
\text{recruit}_{k, i} \leq \text{recruit}_{k}, \quad \forall k, i
\]

3. Overmanning limits:
\[
\sum_{k=1}^{K} \text{overmanning}_{k, i} \leq \text{num\_overman}, \quad \forall i
\]

4. Short-time working limits:
\[
\text{short}_{k, i} \leq \text{num\_shortwork}, \quad \forall k, i
\]

5. Non-negativity constraints:
\[
\text{recruit}_{k, i}, \text{overmanning}_{k, i}, \text{short}_{k, i} \geq 0, \quad \forall k, i
\]

\end{document}</MATH_MODEL>
<DATA>
{'requirement': [[1000, 1400, 1000], [500, 2000, 1500], [0, 2500, 2000]], 'strength': [2000, 1500, 1000], 'lessonewaste': [0.25, 0.2, 0.1], 'moreonewaste': [0.1, 0.05, 0.05], 'recruit': [500, 800, 500], 'costredundancy': [200, 500, 500], 'num_overman': 150, 'costoverman': [1500, 2000, 3000], 'num_shortwork': 50, 'costshort': [500, 400, 400]}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Extract data from the JSON format
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

#### Constants
K = len(data['strength'])  #### Number of manpower categories
I = len(data['requirement'][0])  #### Number of years

#### Create a Linear Programming problem
problem = pulp.LpProblem("Manpower_Optimization", pulp.LpMinimize)

#### Decision Variables
recruit = pulp.LpVariable.dicts("recruit", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
overmanning = pulp.LpVariable.dicts("overmanning", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')
short = pulp.LpVariable.dicts("short", ((k, i) for k in range(K) for i in range(I)), lowBound=0, cat='Continuous')

#### Objective function
problem += pulp.lpSum(
    data['costredundancy'][k] * recruit[k, i] +
    data['costoverman'][k] * overmanning[k, i] +
    data['costshort'][k] * short[k, i]
    for k in range(K) for i in range(I)
)

#### Constraints

#### Manpower requirements
for k in range(K):
    for i in range(I):
        problem += (
            data['strength'][k] - 
            data['lessonewaste'][k] * recruit[k, i] - 
            data['moreonewaste'][k] * data['strength'][k] + 
            recruit[k, i] + 
            short[k, i] + 
            overmanning[k, i] >= data['requirement'][k][i]
        )

#### Recruitment limits
for k in range(K):
    for i in range(I):
        problem += recruit[k, i] <= data['recruit'][k]

#### Overmanning limits
for i in range(I):
    problem += pulp.lpSum(overmanning[k, i] for k in range(K)) <= data['num_overman']

#### Short-time working limits
for k in range(K):
    for i in range(I):
        problem += short[k, i] <= data['num_shortwork']

#### Solve the problem
problem.solve()

#### Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```

