import pandas as pd
import numpy as np

# const
# (4.1-4.4)
n = 1.2
m1 = 0.8
m3 = 1

# (6.1)
k = 1


def conditionME075(R_H_1, R_H_2, m2, m3):
    return (R_H_2 * m3) / (R_H_1 * m2) >= .75


# ОСТ 153-39.4-010-2002 | 8 страница (4.1) (4.2)
def pipe_wall_thickness_for_decommissioning(R_H_1: float, R_H_2: float, P: float, alfa: float, D_h: float, k1: float,
                                            m2: float) -> float:
    """
    R1: расчётное сопротивление материала труб и деталей трубопровода, Па
    :param R_H_1: нормативное сопротивление, равное наименьшему значению пре менного сопротивления разрыву материала
    труб, принимаемое по ГОСТу или ТУ на соответствующие виды труб. Па
    :param R_H_2: нормативное сопротивление, равное наименьшему значению предела текучести при растяжении, сжатии и
    изгибе материала труб, принимаемое по ГОСТу или ТУ на соответствующие трубы. Па
    :param m2: коэффициент условий работы трубопровода, величина которого принимается в зависимости от транспортируемой
    фель для токсичных, горю чих, взрывоопасных и сжиженных газов 0,6; для инертных газов (ают, воздух и т.п.) или
    токсичных, горючих, взрывоопасных жидкостей 0,75; для инерт ных жидкостей 0.9:
    m3: кэффициент условий работы материала труб при повышенных тем пературах, для условий работы промысловых
    трубопроводов
    n: const
    :param P: рабочее давление в трубопроводе, Па
    :param alfa: коэффициент несущей способности, см. спецификацию
    :param D_h: наружный диаметр трубы или детали трубопровода, м
    m1: const
    :param k1: коэффициент однородности материала труб: для бесшовных труб из углеродистой и для сварных труб из
    низколегированной ненормализованной стали к 0,8, для сварных труб из углеродистой и для сварных труб из
    нормализованной низколегированной стали к, 0,85
    :return:толщина стенки трубы или детали трубопровода при которой они должны быть изъяты из
    эксплуатации, м
    """
    if conditionME075(R_H_1, R_H_2, m2, m3):
        R1 = R_H_1 * m1 * m2 * k1
        pipe_wall_thickness = (n * P * alfa * D_h) / (2 * (R1 + n * P))
    else:
        pipe_wall_thickness = (n * P * alfa * D_h) / (2 * (0.9 * R_H_2 * m3 + n * P))
    return pipe_wall_thickness


# допустимое давление ОСТ 153-39.4-010-2002 | 9 страница (4.3) (4.4)
def permissible_pressure_func(t: float, R_H_2: float, R_H_1: float, m2: float, alfa: float, D_n: float,
                              k1: float) -> float:
    """
    :param t: толщина стенки трубы, м (не указано)
    :param R_H_2: нормативное сопротивление, равное наименьшему значению предела текучести при растяжении, сжатии и
    изгибе материала труб, принимаемое по ГОСТу или ТУ на соответствующие трубы. Па
    :param R_H_1:нормативное сопротивление, равное наименьшему значению пре менного сопротивления разрыву материала
    труб, принимаемое по ГОСТу или ТУ на соответствующие виды труб. Па
    :param m2: коэффициент условий работы трубопровода, величина которого принимается в зависимости от транспортируемой
    фель для токсичных, горю чих, взрывоопасных и сжиженных газов 0,6; для инертных газов (ают, воздух и т.п.) или
    токсичных, горючих, взрывоопасных жидкостей 0,75; для инерт ных жидкостей 0.9:
    :param alfa: коэффициент несущей способности, см. спецификацию
    :param D_n: наружный диаметр трубы или детали трубопровода, м
    :param k1: коэффициент однородности материала труб: для бесшовных труб из углеродистой и для сварных труб из
    низколегированной ненормализованной стали к 0,8, для сварных труб из углеродистой и для сварных труб из
    нормализованной низколегированной стали к, 0,85
    :return: допустимое давление
    """
    if conditionME075(R_H_1, R_H_2, m2, m3):
        R1 = R_H_1 * m1 * m2 * k1
        permissible_pressure = (2 * t * R1) / (n * (alfa * D_n - 2 * t))
    else:
        permissible_pressure = (1.8 * R_H_2 * m3) / (n * (alfa * D_n - 2 * t))
    return permissible_pressure


# Расчёты напряжённо-деформированного состояния трубопроводов
# ОСТ 153-39.4-010-2002 | 16 страница (6,1) Проверочный расчет толщины стенки трубопровода, а также её
# определение в случае ремонта
def check_calculation_of_pipeline_wall_thickness(gamma_f: float, P: float, D_h: float,
                                                 contains_hydrogen_sulfide: bool, R_H_1: float, R_H_2: float,
                                                 m2: float, gamma_m: float, gamma_n: float, gamma_s: float) -> float:
    """
    :param gamma_f:
    k: коэффициент несущей способности труб и соединительных до талей, значение которого принимается согласно
    СП 34-116-97 (для труб, заглушек и переходов - 1)
    :param P: -//-
    :param D_h: -//-
    :param contains_hydrogen_sulfide:
    :param R_H_1: -//-
    :param R_H_2: -//-
    :param m2: коэффициент условий работы трубопровода
    :param gamma_m: коэффициент надежности по материалу
    :param gamma_n: коэффициент надежности по назначению трубопроводов
    :param gamma_s: коэффициент надежности по нагрузке
    :return: расчет толщины стенки трубопровода
    """
    if contains_hydrogen_sulfide:
        R = min((R_H_1 * m2) / (gamma_m * gamma_n), (R_H_2 * m2) / (0.9 * gamma_n))
    else:
        R = R_H_2 * gamma_s / gamma_n
    calculation_of_pipeline_thickness = (gamma_f * k * P * D_h) / (2 * (R + 0.6 * gamma_f * P))
    return calculation_of_pipeline_thickness


# (6.2)
# Проверка общей устойчивости подземного трубопровода в продольном направлении
def checking_stability_of_underground_pipeline_in_longitudinal_direction(S: float, m2: float, N_cp: float) -> bool:
    """
    :param S: эквивалентное продольное осевое усилие в трубопроводе, возникаю шее от действия расчетных нагрузок и
    воздействий с учетом продольных и поперечных перемещений трубопровода
    :param m2: коэффициент условий работы трубопровода
    :param N_cp: продольное критическое усилие, при котором наступает потеря про- дольной устойчивости трубопровода,
    с учетом принятого конструктивного ре шения трубопровода.
    :return: Проверка общей устойчивости подземного трубопровода в продольном направлении
    """
    return S <= m2 * N_cp


# Расчёт остаточного ресурса трубопровода по минимальной вероят ной толщине стенки труб по результатам диагностики
# ОСТ 153-39.4-010-2002 | 19 страница (7.1)
def standard_deviation_sigma(N: int, t_k: list, t_cp: float) -> float:
    """
    :param N: число участков замера
    :param t_k: результаты измерений толщин нак-х участках поверхности
    :param t_cp: средняя измеренная толщина
    :return: Среднее квадратическое отклонение
    """
    sum_of_squares = 0
    for k in range(N):
        sum_of_squares += (t_k[k] - t_cp) ** 2
    sigma = (sum_of_squares / (N - 1)) ** .5
    return sigma


# (7.2)
# Минимальную возможную толщину стенки с учетом пеконтролиро ванных участко в поверхности определяют для доверительной
# вероятности 95% применительно но всем промысловым трубопроводам по формуле
def minimum_possible_wall_thickness(t_cp: float, sigma: float, t_k: list, increased_accuracy: bool = False) -> float:
    """
    :param t_cp: средняя измеренная толщина
    :param sigma: Среднее квадратическое отклонение
    :return: Минимальную возможную толщину стенки
    """
    t_min = t_cp - 2 * sigma
    if increased_accuracy:
        for i in t_k:
            t_min = min(t_min, i)
    return t_min


# (7.3)
# Средняя скорость коррозии стенки трубопровода
def average_corrosion_rate_of_pipeline_wall(t_n: float, t_min: float, tau: float) -> float:
    """
    :param t_n: номинальная толщина стенки
    :param t_min: Минимальную возможную толщину стенки
    :param tau: время эксплуатации трубопровода, лет
    :return: Средняя скорость коррозии стенки трубопровода
    """
    V_cp = (t_n - t_min) / tau
    return V_cp


# (7,4)
# Остаточный ресурс трубопровода
def residual_life_of_pipeline(t_min: float, t_otb: float, V_cp: float) -> float:
    """
    :param t_min: Минимальную возможную толщину стенки
    :param t_otb: толщина стенки трубы или детали трубопровода, м, при которой они должны быть изъяты из эксплуатации
    :param V_cp: Средняя скорость коррозии стенки трубопровода
    :return:
    """
    tau_ost = (t_min - t_otb) / V_cp
    return tau_ost


# ОСТ 153-39.4-010-2002 | 20 страница (8.1)
# Вероятностный расчёт остаточного ресурса с учётом общего коррозионно-зрозненного износа стенки трубы
def internal_pressure_pipeline_element_can_withstand(t_n, delta_0, delta, R_H_1, m2, k1, alfa, D_n) -> float:
    """
    t: Текущую толщину стенки
    :param k1: -//-
    :param m2: -//-
    :param R_H_1: -//-
    :param t_n: номинальная толщина стенки
    :param delta_0: начальное технологическое изменение толщины стенки
    :param delta: износ стени
    :param alfa:-//-
    :param D_n:-//-
    :return:
    """
    t = t_n - delta_0 - delta
    R1 = R_H_1 * m1 * m2 * k1
    P_0 = (2 * t * R1) / (n * alfa * D_n)
    return P_0

#(8.2)
#P_0_n = internal_pressure_pipeline_element_can_withstand(...)
def have_pipeline_strength_during_operation(P_0_n, delta_0, delta, t_n, P) -> bool:
    """
    :param P_0_n: внутреннее давление которое может выдержать элемент трубопровода
    :param delta_0: -//-
    :param delta: -//-
    :param t_n: -//-
    :param P: рабочее давление
    :return:
    """
    delta_0_ = delta_0 / t_n
    delta_ = delta / t_n
    return P_0_n * (1 - delta_0_ - delta_) >= P

