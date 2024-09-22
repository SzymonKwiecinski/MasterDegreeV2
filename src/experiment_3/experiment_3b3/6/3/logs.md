# START: OR_C 
## START ROLE MESSAGE | Role.SYSTEM 
Background: You are a expert at Operations Research and Linear Programming and Latex. You create mathematical model of given problem in LATEX format. Latex code place between ```latex and ``` Remember to add 'documentclass{article},usepackage{amsmath},begin{document}, end{document} in latex file. 
## START MESSAGE 0 
### ROLE: Role.USER
<DESCRIPTION>
PROBLEM TYPE: LP

PROBLEM INFO: 

- A state wants to plan its electricity capacity for the next \var{T} years. 
- The state has a forecast of \var{demand_t} megawatts, presumed accurate, of the demand for electricity during year \var{t}.
- The existing capacity, which is in oil-fired plants, that will not be retired and will be available during year \var{t}, is \var{oil_t}.
- There are two alternatives for expanding electric capacity: coal­ fired or nuclear power plants.
- There is a capital cost of \var{coal_cost} per megawatt of coal-fired capacity that becomes operational at the beginning of year \var{t}.
- There is a capital cost of \var{nuke_cost} per megawatt of nuclear power capacity that becomes operational at the beginning of year \var{t}.
- For various political and safety reasons, it has been decided that no more than \var{max_nuke}% of the total capacity should ever be nuclear (\var{max_nuke} is a number between 0 and 100).
- Coal plants last for \var{coal_life} years, while nuclear plants last for \var{nuke_life} years.

INPUT FORMAT: 

{
    "demand": [demand_t for t in 1, ..., T],
    "oil_cap": [oil_t for t in 1, ..., T],
    "coal_cost": coal_cost,
    "nuke_cost": nuke_cost,
    "max_nuke": max_nuke,
    "coal_life": coal_life,
    "nuke_life": nuke_life,
}


OBJECTIVE: What is the capacity expansion plan that results in the minimum cost?


OUTPUT INFO:

- the output should represent how much coal and nuclear capacity should be added in each year, and how much the total cost is.
- the output should be a dictionary with three keys: "coal_cap_added", "nuke_cap_added", and "total_cost".
- the value of "coal_cap_added" should be a list of the coal capacity added in each year.
- the value of "nuke_cap_added" should be a list of the nuclear capacity added in each year.
- the value of "total_cost" should be a single floating point number showing the total cost of the system.


OUTPUT FORMAT:

{
    "coal_cap_added": [coal_t for t in 1, ..., T],
    "nuke_cap_added": [nuke_t for t in 1, ..., T],
    "total_cost": total_cost,
}


</DESCRIPTION>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```latex
\documentclass{article}
\usepackage{amsmath}
\begin{document}

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{c,t} \): Amount of coal-fired capacity added in year \( t \) (in megawatts)
    \item \( x_{n,t} \): Amount of nuclear power capacity added in year \( t \) (in megawatts)
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item \( T \): Number of years
    \item \( d_t \): Demand for electricity in year \( t \) (in megawatts)
    \item \( o_t \): Existing oil-fired capacity in year \( t \) (in megawatts)
    \item \( C_c \): Capital cost of coal-fired capacity (per megawatt)
    \item \( C_n \): Capital cost of nuclear power capacity (per megawatt)
    \item \( M_n \): Maximum allowable percentage of total capacity that can be nuclear (percentage)
    \item \( L_c \): Lifespan of coal-fired plants (in years)
    \item \( L_n \): Lifespan of nuclear plants (in years)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \left( C_c \cdot x_{c,t} + C_n \cdot x_{n,t} \right)
\]

\subsection*{Constraints}
1. Capacity availability constraint:
\[
o_t + \sum_{j=\max(1, t-L_c+1)}^{t} x_{c,j} + \sum_{j=\max(1, t-L_n+1)}^{t} x_{n,j} \geq d_t \quad \forall t = 1, \ldots, T
\]

2. Maximum nuclear capacity constraint:
\[
\sum_{j=1}^{t} x_{n,j} \leq \frac{M_n}{100} \left( o_t + \sum_{j=1}^{t} x_{c,j} + \sum_{j=1}^{t} x_{n,j} \right) \quad \forall t = 1, \ldots, T
\]

3. Non-negativity constraints:
\[
x_{c,t} \geq 0, \quad x_{n,t} \geq 0 \quad \forall t = 1, \ldots, T
\]

\subsection*{Output Format}
The output should provide the following:
\begin{itemize}
    \item \texttt{coal\_cap\_added}: List of coal capacity added in each year.
    \item \texttt{nuke\_cap\_added}: List of nuclear capacity added in each year.
    \item \texttt{total\_cost}: Total cost of the system.
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

\section*{Linear Programming Model for Electricity Capacity Expansion}

\subsection*{Variables}
Let:
\begin{itemize}
    \item \( x_{c,t} \): Amount of coal-fired capacity added in year \( t \) (in megawatts)
    \item \( x_{n,t} \): Amount of nuclear power capacity added in year \( t \) (in megawatts)
\end{itemize}

\subsection*{Parameters}
Given:
\begin{itemize}
    \item \( T \): Number of years
    \item \( d_t \): Demand for electricity in year \( t \) (in megawatts)
    \item \( o_t \): Existing oil-fired capacity in year \( t \) (in megawatts)
    \item \( C_c \): Capital cost of coal-fired capacity (per megawatt)
    \item \( C_n \): Capital cost of nuclear power capacity (per megawatt)
    \item \( M_n \): Maximum allowable percentage of total capacity that can be nuclear (percentage)
    \item \( L_c \): Lifespan of coal-fired plants (in years)
    \item \( L_n \): Lifespan of nuclear plants (in years)
\end{itemize}

\subsection*{Objective Function}
Minimize the total cost:
\[
\text{Minimize } Z = \sum_{t=1}^{T} \left( C_c \cdot x_{c,t} + C_n \cdot x_{n,t} \right)
\]

\subsection*{Constraints}
1. Capacity availability constraint:
\[
o_t + \sum_{j=\max(1, t-L_c+1)}^{t} x_{c,j} + \sum_{j=\max(1, t-L_n+1)}^{t} x_{n,j} \geq d_t \quad \forall t = 1, \ldots, T
\]

2. Maximum nuclear capacity constraint:
\[
\sum_{j=1}^{t} x_{n,j} \leq \frac{M_n}{100} \left( o_t + \sum_{j=1}^{t} x_{c,j} + \sum_{j=1}^{t} x_{n,j} \right) \quad \forall t = 1, \ldots, T
\]

3. Non-negativity constraints:
\[
x_{c,t} \geq 0, \quad x_{n,t} \geq 0 \quad \forall t = 1, \ldots, T
\]

\subsection*{Output Format}
The output should provide the following:
\begin{itemize}
    \item \texttt{coal\_cap\_added}: List of coal capacity added in each year.
    \item \texttt{nuke\_cap\_added}: List of nuclear capacity added in each year.
    \item \texttt{total\_cost}: Total cost of the system.
\end{itemize}

\end{document}</MATH_MODEL>
<DATA>
{'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 'CoalLife': 5, 'NukeLife': 10}</DATA>


## START MESSAGE 1 
### ROLE: Role.ASSISTANT
```python
import pulp

#### Data
data = {'T': 12, 'Demand': [10, 15, 17, 20, 13, 19, 10, 25, 30, 33, 30, 35], 
        'OilCap': [15, 14, 13, 10, 10, 7, 5, 5, 5, 5, 5, 5], 
        'CoalCost': 10, 'NukeCost': 5, 'MaxNuke': 20, 
        'CoalLife': 5, 'NukeLife': 10}

#### Unpack data
T = data['T']
demand = data['Demand']
oil_cap = data['OilCap']
C_c = data['CoalCost']
C_n = data['NukeCost']
M_n = data['MaxNuke']
L_c = data['CoalLife']
L_n = data['NukeLife']

#### Problem
problem = pulp.LpProblem("Electricity_Capacity_Expansion", pulp.LpMinimize)

#### Variables
x_c = pulp.LpVariable.dicts("Coal_Added", range(T), lowBound=0, cat='Continuous')
x_n = pulp.LpVariable.dicts("Nuke_Added", range(T), lowBound=0, cat='Continuous')

#### Objective Function
problem += pulp.lpSum(C_c * x_c[t] + C_n * x_n[t] for t in range(T)), "Total_Cost"

#### Constraints
for t in range(T):
    #### Capacity availability constraint
    problem += (oil_cap[t] + pulp.lpSum(x_c[j] for j in range(max(0, t-L_c+1), t+1)) + 
                pulp.lpSum(x_n[j] for j in range(max(0, t-L_n+1), t+1))) >= demand[t]

    #### Maximum nuclear capacity constraint
    problem += pulp.lpSum(x_n[j] for j in range(t+1)) <= (
            M_n / 100.0 * (oil_cap[t] + pulp.lpSum(x_c[j] for j in range(t+1)) + 
            pulp.lpSum(x_n[j] for j in range(t+1))))

#### Solve the problem
problem.solve()

#### Collect results
coal_cap_added = [pulp.value(x_c[t]) for t in range(T)]
nuke_cap_added = [pulp.value(x_n[t]) for t in range(T)]
total_cost = pulp.value(problem.objective)

#### Output results
print("Coal Capacity Added:", coal_cap_added)
print("Nuclear Capacity Added:", nuke_cap_added)
print("Total Cost:", total_cost)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
```


