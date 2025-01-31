import pandas as pd
import numpy as np
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def bond_pricing(face_value, coupon_rate, freq, yield_to_maturity, purchase_date, next_coupon_date, maturity_date):

    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    next_coupon_date = datetime.strptime(next_coupon_date, "%Y-%m-%d")
    maturity_date = datetime.strptime(maturity_date, "%Y-%m-%d")

    starting_date = purchase_date
    date_rows = [next_coupon_date]
    while starting_date < maturity_date:
        if freq == 1:
            starting_date = starting_date.replace(year=(starting_date.year + 1))
            date_rows.append(starting_date)
        elif freq == 2:
            starting_date = starting_date + relativedelta(months=6)
            date_rows.append(starting_date)
        else:
            raise ValueError("Compounding frequency can only be annual (1) or semiannual (2).")

    t_list = []
    for x in date_rows:
        t_list.append((x - purchase_date).days / 365)

    date_rows = [dt.strftime("%Y-%m-%d") for dt in date_rows]

    c_rows = []
    for x in t_list:
        c_rows.append(np.round(face_value * coupon_rate, 2))
    c_rows[-1] += face_value

    pv_rows = []
    for x, y in zip(c_rows, t_list):
        pv_rows.append(np.round(x / (1 + yield_to_maturity) ** y, 2))

    payments_data = [date_rows, c_rows, pv_rows]
    payments_columns = ["Payment Date", "Coupon", "Present Value"]
    payments_df = pd.DataFrame(payments_data, payments_columns)
    payments_df = payments_df.transpose()

    pv_times_t = []
    for x, y in zip(pv_rows, t_list):
        pv_times_t.append(x * y)

    tsquared = []
    for x in t_list:
        tsquared.append(x ** 2)

    pv_times_t_squared = []
    for x, y in zip(pv_times_t, tsquared):
        pv_times_t_squared.append(x * y)

    calculations_data = [t_list, pv_times_t, tsquared, pv_times_t_squared]
    calculations_columns = ["t", "PV * t", "t^2", "PV * t^2"]
    calculations_df = pd.DataFrame(calculations_data, calculations_columns)
    calculations_df = calculations_df.transpose()

    if freq == 1:
        last_coupon_date = next_coupon_date.replace(year=(next_coupon_date.year - 1))
    elif freq == 2:
        last_coupon_date = next_coupon_date - relativedelta(months=6)

    accrued_interests = np.round((purchase_date - last_coupon_date).days * coupon_rate * face_value / 365, 2)
    dirty_price = np.round(sum(payments_df["Present Value"]), 2)
    clean_price = np.round(dirty_price - accrued_interests, 2)
    mc_duration = np.round(sum(calculations_df["PV * t"]) / clean_price, 2)
    m_duration = np.round(mc_duration / (1 + yield_to_maturity), 2)
    convexity = np.round(sum(calculations_df["PV * t^2"]) / clean_price, 2)

    pricing_data = [dirty_price, accrued_interests, clean_price, mc_duration, m_duration, convexity]
    pricing_columns = ["Dirty Price", "Accrued Interests", "Clean Price", "Macaulay Duration", "Modified Duration",
                       "Convexity"]

    pricing_df = pd.DataFrame(pricing_data, pricing_columns)

    return payments_df, pricing_df

