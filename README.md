# 🌐 Orquestador de Infraestructura en AWS con GitHub Actions 🚀

Este proyecto automatiza el despliegue de una infraestructura completa en AWS utilizando **GitHub Actions** y **Terraform**. La solución incluye:

- Creación de un bucket S3
- Subida de un archivo CSV
- Despliegue de una función Lambda en Python
- Ejecución automática de la función Lambda para procesar el archivo

---

## 📦 Repositorios involucrados

Este orquestador coordina varios repositorios de GitHub para una infraestructura modular:

| Repositorio      | Contenido                                                   |
|------------------|-------------------------------------------------------------|
| `FEGF-project`   | Archivos de datos (como `kc_house_datcsv.csv`)              |
| `FEGF-s3`        | Código Terraform para crear y gestionar el bucket S3        |
| `FEGF-lambda`    | Código Python y Terraform para la función Lambda            |

---

## ⚙️ Flujo automatizado del workflow

El archivo `deploy.yaml` ubicado en `.github/workflows/` define los pasos que GitHub ejecuta automáticamente:

1. 🛠️ **Instala Terraform en la máquina virtual**
2. 📁 **Clona los tres repositorios necesarios**
3. ☁️ **Crea el bucket S3 con Terraform**
4. 📤 **Sube el archivo CSV al bucket**
5. 🧠 **Despliega la función Lambda desde código Python comprimido**
6. 🚀 **Ejecuta la función Lambda y muestra el resultado**

---

## 🧾 Detalles del archivo Workflow (`deploy.yaml`)

```yaml
name: Orquestador de infraestructuraa

on:
  push:
    branches:
      - main

jobs:
  orquestar-todo:
    runs-on: ubuntu-latest

    steps:
      - name: Instalar Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.7

      - name: Clonar FEGF-project
        uses: actions/checkout@v3
        with:
          repository: GaryFernandoYM/FEGF-project
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          path: project

      - name: Clonar FEGF-s3
        uses: actions/checkout@v3
        with:
          repository: GaryFernandoYM/FEGF-s3
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          path: s3

      - name: Clonar FEGF-lambda
        uses: actions/checkout@v3
        with:
          repository: GaryFernandoYM/FEGF-lambda
          token: ${{ secrets.PERSONAL_ACCESS_TOKEN }}
          path: lambda

      - name: Deploy S3 con Terraform
        run: |
          cd s3
          terraform init
          terraform apply -auto-approve -var="bucket_name=bucket-lambda-s3-fegf"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1

      - name: Subir archivo CSV al bucket S3
        run: |
          aws s3 cp ./project/csv/kc_house_datcsv.csv s3://bucket-lambda-s3-fegf/
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1

      - name: Deploy Lambda con Terraform
        run: |
          cd lambda
          zip function.zip lambda_function.py
          terraform init
          terraform apply -auto-approve -var="function_name=lambda-s3-fegf" -var="bucket_name=bucket-lambda-s3-fegf"
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1

      - name: Ejecutar la función Lambda
        run: |
          aws lambda invoke \
            --function-name lambda-s3-fegf \
            --invocation-type RequestResponse \
            --payload '{}' \
            response.json
          cat response.json
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_DEFAULT_REGION: us-east-1
