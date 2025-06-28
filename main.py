import pandas as pd

csv_path = "kc_house_datcsv.csv"

df = pd.read_csv(csv_path, header=None, sep=',', quotechar='"', engine='python')

df = df.drop(index=0).reset_index(drop=True)

df.columns = [
    "id", "date", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot",
    "floors", "waterfront", "view", "condition", "grade", "sqft_above",
    "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long",
    "sqft_living15"
]

json_output = df.to_json(orient='records', lines=True)

with open("kc_house_data.json", "w") as f:
    f.write(json_output)

print("Conversión exitosa. Archivo guardado como 'kc_house_data.json'")
