import pandas as pd

df = pd.read_csv("wineries.csv")
chunks = df.apply(lambda row: f"{row['Winery Name']} offers {row['Wine Specialties']} at {row['Address']} (Max group: {row['max group size']}, Tasting: ${row['Tasting Price']})", axis=1).tolist()
