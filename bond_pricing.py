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

