# 🏦 Sistema de Predicción de Abandono Fintech

Un sistema integral de aprendizaje automático para predecir el abandono de clientes con un panel interactivo, API en tiempo real e insights impulsados por IA.

## 🌟 Fundamentación
 - Ver: "Documentos/Análisis del Churn en Fintech.docx "

## 🌟 Características

### Datos Utilizados
- Datos originales crudos: "churn_data.csv" (Dataset de Kaggle).
- Datos limpios : "Fintech_user_limpio.csv"
- Ver: "Documentos/Significado de los datos.doc"


### Jupyter Notebooks
- Notebook EDA:
  **Exploración y Estadísticas Descriptivas:**
      -  "Notebooks/Fintech_churn.ipynb"
- Notebooks de Machine Learning: 
  **Clasificadores XGBoost y Random Forest para predicción de abandono y Explicación de modelos con SHAP.** 
      -  "Notebooks/churn_final.ipynb"
  **Clasificador Red Neuronal para predicción de abandono y Explicación de modelo con SHAP**   
      -  "Notebooks/Dataset_sintetico_red_neuronal.ipynb"

   Estos notebooks generan los modelos entrenados en formato pkl que son incorporados a la api para inferencia en tiempo real.
 
### API REST basada en FastAPI para predicciones en tiempo real
  - "api.py"
  Recibe un POST con los datos de un cliente, invoca los modelos desde sus archivos pkl, hace la predicción y entrega un objeto JSON con los resultados de las predicciones de los modelos RF y XGB:
   - Probabilidad de churn %
   - Predicción de churn: Si (1) o No (0)
   - Nivel de riesgo (Bajo/Medio/Alto)
   - Valores SHAP (Explicabilidad de las predicciones) Lista de importancia de variables en la predicción.  


### Paneles Interactivos

**Panel Streamlit** (`streamlit_ui.py`)
- 🎨 Interfaz web 
- 📊 Tablas de datos interactivas con AgGrid
- 📈 Visualizaciones avanzadas con Plotly
- 🎯 Gráficos de radar de perfil de cliente
- 🔢 Indicadores de medidor de riesgo



**Motor de Insights de IA** (`llm_api.py` )
API REST basada en FastAPI para predicciones en tiempo real
  
  Recibe un POST con los datos de un cliente más los datos de salida del modelo predictivo y entrega un objeto 
  InsightResponse con: recommendations, key_insights y action_items.
  Se probó con modelos preentrenados pequeños del Hub de Hugging Face: "distilgpt2", "gpt2",  "microsoft/DialoGPT-small", "microsoft/Phi-3-mini-4k-instruct",

   - Recomendaciones de retención de clientes impulsadas por LLM
   - Elementos de acción personalizados basados en el perfil del cliente
   - Estrategias de intervención basadas en riesgo
   - Análisis de patrones de comportamiento


## 🚀 Inicio Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements4.txt
```

### 2. Los modelos de Machine Learning y sus Explainers SHAP se encuentran en los siguientes archivos:

      Modelos/RandomForest_model.pkl
      Modelos/RandomForest_model_explainer.pkl
      Modelos/XGBoost_model.pkl
      Modelos/XGBoost_model_explainer.pkl


### 3. Iniciar Todos los Servicios

** Api de predicciones**
```bash
python api.py
```

** UI de Streamlit**
```bash
python run_streamlit.py
```

Esto inicia:
- 🤖 API de Predicción de Abandono (puerto 8000)
- 📊 Panel (Streamlit: puerto 8501)

### 4. Acceder al Panel

- **Streamlit**: `http://localhost:8501`

## 🎮 Usando los Paneles


### Características del Panel Streamlit
1. **📊 Pestaña de Datos de Clientes**
   - Tabla de datos interactiva con ordenamiento y filtrado
   - Selección de clientes con casillas de verificación
   - Estadísticas de resumen en tiempo real
   - Barra lateral de filtrado avanzado

2. **➕ Pestaña Agregar Cliente**
   - Formulario integral de cliente
   - Todos los 30+ atributos de cliente
   - Generación automática de información personal
   - Validación de formulario

3. **🤖 Pestaña de Predicciones**
   - Visualización del perfil del cliente
   - Predicción de abandono en tiempo real
   - Indicadores de nivel de riesgo con codificación de colores
   - Gráficos de explicabilidad SHAP
   - Barras de progreso y medidores

4. **💡 Pestaña de Insights**
   - Estrategias de retención basadas en reglas e impulsadas por IA
   - Visualización de medidor de riesgo
   - Recomendaciones personalizadas
   - Insights orientados a la acción

5. **📊 Pestaña de Análisis Masivo**
   - Procesamiento de múltiples clientes simultáneamente
   - Predicciones e insights en lote
   - Exportación de resultados a CSV
   - Métricas de rendimiento de campaña

6. **📧 Pestaña de Email Marketing**
   - Campañas de email personalizadas basadas en riesgo
   - Segmentación automática de clientes
   - Plantillas HTML profesionales
   - Múltiples formatos de exportación

## Endpoints de API

### POST /predict
Predice la probabilidad de abandono para un cliente.

**Ejemplo de cuerpo de solicitud:**
```json
{
  "age": 35,
  "housing": "own",
  "credit_score": 650.5,
  "deposits": 5,
  "withdrawal": 3,
  "purchases_partners": 10,
  "purchases": 25,
  "cc_taken": 1,
  "cc_recommended": 0,
  "cc_disliked": 0,
  "cc_liked": 1,
  "cc_application_begin": 1,
  "app_downloaded": 1,
  "web_user": 1,
  "app_web_user": 1,
  "ios_user": 1,
  "android_user": 0,
  "registered_phones": 1,
  "payment_type": "credit_card",
  "waiting_4_loan": 0,
  "cancelled_loan": 0,
  "received_loan": 1,
  "rejected_loan": 0,
  "zodiac_sign": "leo",
  "left_for_two_month_plus": 0,
  "left_for_one_month": 0,
  "rewards_earned": 150,
  "reward_rate": 0.02,
  "is_referred": 1
}
```

**Respuesta:**
```json
{
  "churn_probability": 0.2345,
  "churn_prediction": 0,
  "risk_level": "Low"
}
```

### GET /health
Verifica el estado de salud de la API.

### GET /model-info
Obtiene información sobre el modelo cargado.

## Requisitos de Datos

Tu archivo CSV debe contener estas columnas:
- `user` (integer) - ID de fila, será excluido de las características
- `churn` (integer) - Variable objetivo (0/1)
- `age` (integer)
- `housing` (string)
- `credit_score` (float)
- `deposits` (integer)
- `withdrawal` (integer)
- `purchases_partners` (integer)
- `purchases` (integer)
- `cc_taken` (integer)
- `cc_recommended` (integer)
- `cc_disliked` (integer)
- `cc_liked` (integer)
- `cc_application_begin` (integer)
- `app_downloaded` (integer)
- `web_user` (integer)
- `app_web_user` (integer)
- `ios_user` (integer)
- `android_user` (integer)
- `registered_phones` (integer)
- `payment_type` (string)
- `waiting_4_loan` (integer)
- `cancelled_loan` (integer)
- `received_loan` (integer)
- `rejected_loan` (integer)
- `zodiac_sign` (string)
- `left_for_two_month_plus` (integer)
- `left_for_one_month` (integer)
- `rewards_earned` (integer)
- `reward_rate` (float)
- `is_referred` (integer)

## 📁 Estructura del Proyecto

```
├── Tests                  # Carpeta con tests usados en debugging
├── Documentos             # Carpeta con documentación
├── Datos                  # Carpeta con archivos de datos usados
├── Modelos                # Carpeta con pkl de modelos entrenados 
├── Notebooks              # Carpeta con Notebooks EDA y ML
├── api.py                 # API de predicción de abandono
├── streamlit_ui.py        # Panel Streamlit
├── start_services.py      # Orquestación de servicios
├── run_streamlit.py       # Ejecutor interface de Streamlit
├── requirements4.txt      # Dependencias
└── README.md              # Documentación
```
