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