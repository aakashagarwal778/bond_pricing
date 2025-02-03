# Bond Pricing Calculator  

This repository provides a Python implementation for bond pricing and risk analysis, including the calculation of **dirty price, clean price, accrued interest, Macaulay duration, modified duration, and convexity**.  

## Features  

- Computes **"dirty price"** and **"clean price"** based on bond cash flows.  
- Calculates **"accrued interest"** using coupon frequency (annual/semi-annual).  
- Determines **"Macaulay duration", "modified duration", and "convexity"** for risk assessment.  
- Utilizes present value calculations for accurate pricing.  

## Output  

The function returns two DataFrames:  

- **`payments_df`** – Contains details of future cash flows and their present values.  
- **`pricing_df`** – Summarizes bond pricing metrics.  
