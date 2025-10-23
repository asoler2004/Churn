# 🏦 Sistema de Predicción de Abandono Fintech

Un sistema integral de aprendizaje automático para predecir el abandono de clientes con un panel interactivo, API en tiempo real e insights impulsados por IA.

## 🌟 Características

### Sistema ML Principal
- Clasificador XGBoost para predicción de abandono
- API REST basada en FastAPI para predicciones en tiempo real
- Codificación categórica flexible: LabelEncoder o OneHotEncoder
- Preprocesamiento automático de variables categóricas
- Evaluación del rendimiento del modelo
- Clasificación de nivel de riesgo (Bajo/Medio/Alto)

### Paneles Interactivos
**Panel Taipy** (`churn_ui.py`)
- 📊 Gestión de datos con filtrado y adición de clientes
- 🤖 Interfaz de predicción de abandono en tiempo real
- 💡 Insights de retención de clientes impulsados por IA
- 📈 Gráficos de explicabilidad SHAP
- 🔍 Exploración y análisis de datos de clientes

**Panel Streamlit** (`streamlit_ui.py`)
- 🎨 Interfaz web moderna y responsiva
- 📊 Tablas de datos interactivas con AgGrid
- 📈 Visualizaciones avanzadas con Plotly
- 🎯 Gráficos de radar de perfil de cliente
- 🔢 Indicadores de medidor de riesgo
- 📱 Diseño amigable para móviles

### Motor de Insights de IA
- Recomendaciones de retención de clientes impulsadas por LLM
- Elementos de acción personalizados basados en el perfil del cliente
- Estrategias de intervención basadas en riesgo
- Análisis de patrones de comportamiento

## 🚀 Inicio Rápido

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Entrenar el Modelo
```bash
python train_model.py
```

**Opciones de Codificación:**
- Edita `train_model.py` y establece `use_onehot = True` para OneHotEncoder
- Establece `use_onehot = False` para LabelEncoder (por defecto)

### 3. Iniciar Todos los Servicios

**Opción A: Panel Taipy (Por defecto)**
```bash
python start_services.py
```

**Opción B: Panel Streamlit**
```bash
python start_services.py --ui streamlit
```

**Opción C: Solo Streamlit**
```bash
python run_streamlit.py
```

Esto inicia:
- 🤖 API de Predicción de Abandono (puerto 8000)
- 💡 API de Insights LLM (puerto 8001)  
- 📊 Panel (Taipy: puerto 5000, Streamlit: puerto 8501)

### 4. Acceder al Panel
- **Taipy**: `http://localhost:5000`
- **Streamlit**: `http://localhost:8501`

## 📋 Configuración Manual (Alternativa)

### Entrenar el Modelo
```bash
python train_model.py
```

### Iniciar Servicios Individualmente
```bash
# Terminal 1: API de Predicción de Abandono
python api.py

# Terminal 2: API de Insights LLM  
python llm_api.py

# Terminal 3: Panel Taipy
python churn_ui.py
```

## 🎮 Usando los Paneles

### Características del Panel Taipy
1. **Gestión de Datos**: Cargar datos, aplicar filtros, agregar clientes
2. **Predicción de Abandono**: Seleccionar clientes, ejecutar predicciones, ver resultados
3. **Insights de IA**: Generar recomendaciones de retención impulsadas por LLM

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
   - Estrategias de retención impulsadas por IA
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
├── train_model.py          # Entrenamiento del modelo XGBoost
├── api.py                  # API de predicción de abandono
├── llm_api.py             # API de insights LLM
├── churn_ui.py            # Panel Taipy
├── streamlit_ui.py        # Panel Streamlit
├── test_api.py            # Script de prueba de API
├── start_services.py      # Orquestación de servicios
├── run_streamlit.py       # Ejecutor independiente de Streamlit
├── requirements.txt       # Dependencias
└── README.md             # Documentación
```

## 🗂️ Archivos Generados

- `churn_model.pkl` - Modelo XGBoost entrenado
- `encoders.pkl` - Codificadores ajustados (Label o OneHot)
- `model_metadata.json` - Columnas de características y metadatos de codificación
- `shap_plot.png` - Gráficos de explicabilidad SHAP (cuando se generan)

## 🔧 Endpoints de API

### API de Predicción de Abandono (Puerto 8000)
- `POST /predict` - Predecir abandono para un cliente
- `GET /health` - Verificación de salud
- `GET /model-info` - Información del modelo

### API de Insights LLM (Puerto 8001)
- `POST /generate-insights` - Generar recomendaciones de retención
- `GET /health` - Verificación de salud

## 🎛️ Métodos de Codificación

**LabelEncoder (Por defecto):**
- Convierte categorías a enteros (0, 1, 2...)
- Representación compacta
- Bueno para modelos basados en árboles como XGBoost

**OneHotEncoder:**
- Crea columnas binarias para cada categoría
- Sin suposiciones ordinales
- Mejor para capturar relaciones de categorías

## 🔍 Características del Panel

### Gestión de Datos
- **Carga de CSV**: Cargar datos de clientes desde archivos
- **Generación de Datos Falsos**: Agregar automáticamente columnas de información personal
- **Filtrado en Tiempo Real**: Filtrar por edad, puntaje crediticio, vivienda
- **Adición de Clientes**: Agregar nuevos clientes mediante formulario

### Predicción y Análisis
- **Predicciones ML**: Puntuación de probabilidad de abandono en tiempo real
- **Clasificación de Riesgo**: Niveles de riesgo Bajo/Medio/Alto
- **Explicaciones SHAP**: Visualización de importancia de características
- **Selección de Clientes**: Interfaz de clic para seleccionar

### Insights de IA
- **Estrategias de Retención**: Recomendaciones personalizadas
- **Elementos de Acción**: Pasos específicos de intervención
- **Análisis de Riesgo**: Insights de patrones de comportamiento
- **Perfilado de Clientes**: Análisis integral

### Email Marketing
- **Campañas Personalizadas**: Emails basados en nivel de riesgo del cliente
- **Segmentación Automática**: Clasificación inteligente de clientes
- **Plantillas Profesionales**: Contenido HTML responsivo en español
- **Múltiples Exportaciones**: CSV, HTML, resumen y formato Mailchimp

## 🚨 Solución de Problemas

**Error de Modelo No Encontrado:**
```bash
python train_model.py  # Entrenar el modelo primero
```

**Error de Conexión de API:**
- Asegurar que todos los servicios estén ejecutándose
- Verificar que los puertos 8000, 8001, 5000 estén disponibles
- Usar `python start_services.py` para inicio automático

**Panel No Carga:**
- Verificar instalación de Taipy: `pip install taipy`
- Verificar que el puerto 5000 esté disponible
- Revisar la consola del navegador para errores

**Error de Selectbox Duplicado en Streamlit:**
- Este error se ha corregido agregando claves únicas a todos los elementos selectbox
- Si persiste, reiniciar la aplicación Streamlit

**Problemas de Email Marketing:**
- Verificar que los datos de clientes incluyan campos de email
- Asegurar que el análisis masivo se haya completado para mejores resultados
- Revisar que los filtros de clientes no estén demasiado restrictivos