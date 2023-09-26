from backend_mat_model.data import *
from backend_mat_model.database import *
import pandas as pd
import numpy as np
import json

df = pd.read_csv("Приложение 2. Данные о потоке нефти, газа и воды по каждому трубопроводу.xlsx - Данные для кейса.csv")
df = df.fillna(0)

names = df['Наименование трубопровода']
diameter = df['Ø, мм']
thickness = df['Толщина стенки, мм']
length = df['Длина, м']
P_start = df['вход ']
P_end = df['выход ']
Q_n = df.iloc[:, 7:17]
V_l = df.iloc[:, 17:27]
W = df.iloc[:, 27:37]
Q_g = df.iloc[:, 37:47]
T_cp_n = df.iloc[:, 47:57]
T_cp_k = df.iloc[:, 57:67]
P_cp_n = df.iloc[:, 67:77]
P_cp_k = df.iloc[:, 77:87]


for i in range(len(names)):
    name = names[i]
    param_Qn = [Q_n.iloc[i, k] for k in range(len(Q_n.iloc[i]))]
    param_Qg = [Q_g.iloc[i, k] for k in range(len(Q_g.iloc[i]))]
    # param_Qv = [V_l.iloc[i, k] for k in range(len(V_l.iloc[i]))]
    param_Qv = [i + j for i, j in (param_Qn, param_Qg)]
    param_charge = [W.iloc[i, k] for k in range(len(W.iloc[i]))]#мб то
    param_P = average_pressure_in_area(P_start[i], P_end[i])
    param_T = np.mean(T_cp_n, P_cp_k)
    param_flow_regime = ""
    param_critic_velocity = get_v_kr()

    if existence_of_anti_corrosion_regime():
        param_flow_regime += "антикоррозионный"
    else:
        param_flow_regime += "неантикоррозионный"

    param_critic_velocity_param_factic_velocity = dependence_of_critical_flow_velocity()

    if param_critic_velocity > param_critic_velocity_param_factic_velocity:
        param_flow_regime += " ламинарный"
    else:
        param_flow_regime += "Турбулентный"

    transition = None#что такое

    param_crash = internal_pressure_pipeline_element_can_withstand()#Вероятностный расчёт остаточного ресурса с учётом
    # общего коррозионно-зрозненного износа стенки труб
    param_lifetime = residual_life_of_pipeline() #годы
    dictionary = {
        "name": name,
        "param_charge": param_charge,
        "param_Qn": param_Qn,
        "param_Qg": param_Qg,
        "param_Qv": param_Qv,
        "param_P": param_P,
        "param_T": param_T,
        "param_flow_regime": param_flow_regime,
        "param_critic_velocity_param_factic_velocity": param_critic_velocity_param_factic_velocity,
        "transition": transition,
        "param_crash": param_crash,
        "param_critic_velocity": param_critic_velocity,
        "param_lifetime": param_lifetime
    }
    json_object = json.dumps(dictionary, indent=4)
    with open("example.json", "w") as outfile:
        outfile.write(json_object)

# print(len(P_cp_k.iloc[0]))