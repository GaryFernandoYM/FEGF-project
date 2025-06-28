import pandas as pd

# Ruta del archivo CSV
csv_path = "kc_house_datcsv.csv"

# Leer el archivo sin encabezado y separando correctamente por comas
df = pd.read_csv(csv_path, header=None, sep=',', quotechar='"', engine='python')

# Eliminar la primera fila (que contiene encabezados como datos)
df = df.drop(index=0).reset_index(drop=True)

# Asignar nombres correctos para 20 columnas
df.columns = [
    "id", "date", "price", "bedrooms", "bathrooms", "sqft_living", "sqft_lot",
    "floors", "waterfront", "view", "condition", "grade", "sqft_above",
    "sqft_basement", "yr_built", "yr_renovated", "zipcode", "lat", "long",
    "sqft_living15"
]

# Convertir a JSON en formato por línea (ideal para procesamiento)
json_output = df.to_json(orient='records', lines=True)

# Guardar en archivo JSON
with open("kc_house_data.json", "w") as f:
    f.write(json_output)

print("✅ Conversión exitosa. Archivo guardado como 'kc_house_data.json'")
