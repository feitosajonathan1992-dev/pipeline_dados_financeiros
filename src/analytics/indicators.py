#
# def calculate_financial_indicators(df):
#     df = df.copy()

#     if "ebitda" not in df.columns:
#         return df  # sai sem erro

#     df["ebitda_growth"] = df.groupby("ticker")["ebitda"].pct_change()

#     return df