"""
Ollama Local LLM Integration Module

This module handles all Ollama-specific functionality for generating
AI-powered customer retention insights using local LLM models.
"""

import requests
import json
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel


class OllamaConfig(BaseModel):
    """Configuration for Ollama requests"""
    model: str = "llama3.2"
    temperature: float = 0.7
    top_p: float = 0.9
    max_tokens: int = 1000
    timeout: int = 120  # Increased timeout for model loading
    base_url: str = "http://localhost:11434"


class CustomerInsightRequest(BaseModel):
    """Customer data model for insights generation"""
    age: int
    housing: str
    credit_score: float
    deposits: int
    withdrawal: int
    purchases_partners: int
    purchases: int
    cc_taken: int
    cc_recommended: int
    cc_disliked: int
    cc_liked: int
    cc_application_begin: int
    app_downloaded: int
    web_user: int
    app_web_user: int
    ios_user: int
    android_user: int
    registered_phones: int
    payment_type: str
    waiting_4_loan: int
    cancelled_loan: int
    received_loan: int
    rejected_loan: int
    left_for_two_month_plus: int
    left_for_one_month: int
    rewards_earned: int
    reward_rate: float
    is_referred: int
    churn_probability: float
    churn_prediction: int
    risk_level: str


def check_ollama_status(base_url: str = "http://localhost:11434") -> bool:
    """Check if Ollama is running and available"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_available_models(base_url: str = "http://localhost:11434") -> list:
    """Get list of available Ollama models"""
    try:
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            return [model['name'] for model in models_data.get('models', [])]
        return []
    except:
        return []


def create_comprehensive_customer_profile(customer_data: CustomerInsightRequest) -> str:
    """Create a comprehensive customer profile with all available information"""
    
    # Demographics
    housing_text = {"o": "propia", "r": "alquilada", "na": "no especificada"}.get(customer_data.housing, customer_data.housing)
    payment_text = {
        "monthly": "mensual", 
        "bi-weekly": "quincenal", 
        "weekly": "semanal", 
        "semi-monthly": "bimensual", 
        "na": "no especificado"
    }.get(customer_data.payment_type, customer_data.payment_type)
    
    # Calculate derived metrics
    total_transactions = customer_data.deposits + customer_data.withdrawal + customer_data.purchases + customer_data.purchases_partners
    digital_engagement_score = customer_data.app_downloaded + customer_data.web_user + customer_data.app_web_user + customer_data.ios_user + customer_data.android_user
    credit_product_usage = customer_data.cc_taken + customer_data.received_loan
    
    # Activity patterns
    activity_level = "Alta" if total_transactions > 30 else "Media" if total_transactions > 15 else "Baja"
    digital_adoption = "Completa" if digital_engagement_score >= 3 else "Parcial" if digital_engagement_score >= 1 else "Limitada"
    
    # Risk indicators
    risk_indicators = []
    if customer_data.left_for_one_month:
        risk_indicators.append("Inactivo por 1 mes")
    if customer_data.left_for_two_month_plus:
        risk_indicators.append("Inactivo por 2+ meses")
    if customer_data.cancelled_loan:
        risk_indicators.append("Préstamo cancelado")
    if customer_data.rejected_loan:
        risk_indicators.append("Préstamo rechazado")
    if customer_data.cc_disliked:
        risk_indicators.append("Sentimiento negativo hacia tarjeta de crédito")
    
    # Opportunities
    opportunities = []
    if not customer_data.app_downloaded:
        opportunities.append("Adopción de app móvil")
    if not customer_data.cc_taken and customer_data.credit_score > 650:
        opportunities.append("Oferta de tarjeta de crédito")
    if customer_data.waiting_4_loan:
        opportunities.append("Procesamiento de préstamo pendiente")
    if customer_data.rewards_earned < 100:
        opportunities.append("Activación del programa de recompensas")
    if customer_data.is_referred:
        opportunities.append("Aprovechamiento de red de referidos")
    
    profile = f"""
INFORMACIÓN DEMOGRÁFICA:
• Edad: {customer_data.age} años
• Vivienda: {housing_text}
• Tipo de pago preferido: {payment_text}
• Puntaje crediticio: {customer_data.credit_score:.0f}/850

ACTIVIDAD FINANCIERA:
• Nivel de actividad general: {activity_level} ({total_transactions} transacciones totales)
• Depósitos realizados: {customer_data.deposits}
• Retiros realizados: {customer_data.withdrawal}
• Compras totales: {customer_data.purchases}
• Compras con socios: {customer_data.purchases_partners}
• Teléfonos registrados: {customer_data.registered_phones}

PRODUCTOS Y SERVICIOS:
• Tarjeta de crédito: {'Activa' if customer_data.cc_taken else 'No tomada'}
• Sentimiento hacia TC: {'Positivo' if customer_data.cc_liked else 'Negativo' if customer_data.cc_disliked else 'Neutral'}
• Recomendación de TC: {'Recibida' if customer_data.cc_recommended else 'No recibida'}
• Aplicación de TC iniciada: {'Sí' if customer_data.cc_application_begin else 'No'}
• Estado de préstamo: {'Recibido' if customer_data.received_loan else 'Rechazado' if customer_data.rejected_loan else 'Esperando' if customer_data.waiting_4_loan else 'Cancelado' if customer_data.cancelled_loan else 'Sin actividad'}

ENGAGEMENT DIGITAL:
• Adopción digital: {digital_adoption} (Score: {digital_engagement_score}/5)
• App descargada: {'Sí' if customer_data.app_downloaded else 'No'}
• Usuario web: {'Sí' if customer_data.web_user else 'No'}
• Usuario app+web: {'Sí' if customer_data.app_web_user else 'No'}
• Plataforma iOS: {'Sí' if customer_data.ios_user else 'No'}
• Plataforma Android: {'Sí' if customer_data.android_user else 'No'}

PROGRAMA DE RECOMPENSAS:
• Puntos ganados: {customer_data.rewards_earned}
• Tasa de recompensa: {customer_data.reward_rate:.2%}
• Cliente referido: {'Sí' if customer_data.is_referred else 'No'}

INDICADORES DE RIESGO:
{chr(10).join(f'• {indicator}' for indicator in risk_indicators) if risk_indicators else '• Ningún indicador de riesgo crítico identificado'}

OPORTUNIDADES IDENTIFICADAS:
{chr(10).join(f'• {opportunity}' for opportunity in opportunities) if opportunities else '• Cliente con perfil estable, enfocarse en satisfacción'}

PATRONES DE COMPORTAMIENTO:
• Frecuencia de uso: {'Alta' if total_transactions > 25 else 'Media' if total_transactions > 10 else 'Baja'}
• Preferencia de canal: {'Digital' if digital_engagement_score >= 2 else 'Tradicional'}
• Relación con productos de crédito: {'Positiva' if customer_data.cc_liked or customer_data.received_loan else 'Negativa' if customer_data.cc_disliked or customer_data.rejected_loan else 'Neutral'}
• Nivel de compromiso: {'Alto' if customer_data.rewards_earned > 200 and total_transactions > 20 else 'Medio' if customer_data.rewards_earned > 50 else 'Bajo'}
"""
    
    return profile


def create_enhanced_prompt(customer_data: CustomerInsightRequest) -> str:
    """Create an enhanced prompt with comprehensive customer information"""
    
    customer_profile = create_comprehensive_customer_profile(customer_data)
    
    prompt = f"""Eres un experto analista de retención de clientes fintech con más de 10 años de experiencia. Analiza el siguiente perfil completo del cliente y proporciona insights accionables y específicos para prevenir el abandono.

PERFIL COMPLETO DEL CLIENTE:
{customer_profile}

RIESGO DE ABANDONO: {customer_data.risk_level} (Probabilidad: {customer_data.churn_probability:.1%})

INSTRUCCIONES ESPECÍFICAS:
Proporciona un análisis detallado y estructurado que incluya:

1. INSIGHTS CLAVE (3-4 puntos principales sobre el comportamiento del cliente)
   - Identifica patrones únicos en el comportamiento del cliente
   - Señala fortalezas y debilidades en la relación
   - Destaca factores de riesgo específicos

2. RECOMENDACIONES ESPECÍFICAS (acciones concretas para retener al cliente)
   - Proporciona 4-5 recomendaciones priorizadas
   - Incluye justificación para cada recomendación
   - Considera el perfil específico del cliente

3. ESTRATEGIA DE ENGAGEMENT (cómo aumentar la participación)
   - Canales de comunicación preferidos
   - Productos/servicios a promover
   - Timing óptimo para intervenciones

4. ACCIONES INMEDIATAS (pasos a tomar en las próximas 48 horas)
   - Lista de 3-4 acciones prioritarias
   - Responsables sugeridos para cada acción
   - Métricas de éxito a monitorear

5. SEGUIMIENTO (métricas a monitorear en los próximos 30 días)
   - KPIs específicos del cliente
   - Frecuencia de monitoreo
   - Señales de alerta temprana

CONTEXTO IMPORTANTE:
- Enfócate en soluciones prácticas y personalizadas
- Considera el nivel de riesgo actual del cliente
- Basar recomendaciones en datos específicos del perfil
- Proporcionar justificación clara para cada sugerencia
- Mantener un tono profesional pero empático

Responde en español con un análisis detallado y accionable."""

    return prompt


def generate_ollama_insights(customer_data: CustomerInsightRequest, config: Optional[OllamaConfig] = None) -> Tuple[str, Dict]:
    """Generate insights using Ollama local LLM"""
    
    if config is None:
        config = OllamaConfig()
    
    # Create enhanced prompt with comprehensive customer profile
    prompt = create_enhanced_prompt(customer_data)
    
    try:
        # Make request to Ollama API
        ollama_url = f"{config.base_url}/api/generate"
        
        payload = {
            "model": config.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": config.temperature,
                "top_p": config.top_p,
                "max_tokens": config.max_tokens,
                "stop": ["Human:", "Assistant:", "Usuario:", "Analista:"]
            }
        }
        
        response = requests.post(ollama_url, json=payload, timeout=config.timeout)
        
        if response.status_code == 200:
            result = response.json()
            generated_text = result.get('response', '').strip()
            
            if not generated_text:
                raise Exception("Ollama returned empty response")
            
            # Format the response
            formatted_response = f"""
INSIGHTS GENERADOS POR OLLAMA ({config.model}):

{generated_text}

RESUMEN EJECUTIVO:
• Riesgo de abandono: {customer_data.risk_level} ({customer_data.churn_probability:.1%})
• Prioridad de intervención: {'Alta' if customer_data.risk_level == 'High' else 'Media' if customer_data.risk_level == 'Medium' else 'Baja'}
• Perfil del cliente: {get_customer_profile_summary(customer_data)}

PRÓXIMOS PASOS AUTOMATIZADOS:
1. Implementar recomendaciones principales dentro de 48 horas
2. Configurar alertas de monitoreo para métricas clave
3. Programar seguimiento en 7, 15 y 30 días
4. Evaluar efectividad y ajustar estrategia según respuesta
"""
            
            # Prepare debug information
            debug_info = {
                'prompt': prompt,
                'raw_response': generated_text,
                'model_used': config.model,
                'ollama_url': ollama_url,
                'request_payload': payload,
                'response_status': response.status_code,
                'config': config.dict()
            }
            
            return formatted_response, debug_info
            
        else:
            raise Exception(f"Ollama API error: {response.status_code} - {response.text}")
            
    except requests.exceptions.ConnectionError:
        raise Exception("No se pudo conectar a Ollama. Asegúrate de que Ollama esté ejecutándose en localhost:11434")
    except requests.exceptions.Timeout:
        raise Exception(f"Timeout al conectar con Ollama después de {config.timeout} segundos. El modelo '{config.model}' puede estar cargándose por primera vez. Intenta con un modelo más pequeño como 'llama3.2' o espera unos minutos.")
    except Exception as e:
        raise Exception(f"Error en Ollama: {str(e)}")


def get_customer_profile_summary(customer_data: CustomerInsightRequest) -> str:
    """Generate a brief customer profile summary"""
    
    profile_elements = []
    
    # Age group
    if customer_data.age < 30:
        profile_elements.append("Joven profesional")
    elif customer_data.age > 50:
        profile_elements.append("Cliente maduro")
    else:
        profile_elements.append("Profesional establecido")
    
    # Digital engagement
    if customer_data.app_downloaded and customer_data.web_user:
        profile_elements.append("Usuario digital activo")
    elif not customer_data.app_downloaded:
        profile_elements.append("Oportunidad de digitalización")
    
    # Financial activity
    if customer_data.purchases > 20:
        profile_elements.append("Alto uso de productos")
    elif customer_data.purchases < 10:
        profile_elements.append("Bajo engagement financiero")
    
    # Credit relationship
    if customer_data.cc_taken:
        profile_elements.append("Cliente de crédito")
    
    return ", ".join(profile_elements)


def test_ollama_connection(base_url: str = "http://localhost:11434") -> Dict[str, Any]:
    """Test Ollama connection and return status information"""
    
    try:
        # Test basic connection
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        
        if response.status_code == 200:
            models_data = response.json()
            models = [model['name'] for model in models_data.get('models', [])]
            
            return {
                'status': 'connected',
                'available': True,
                'models': models,
                'model_count': len(models),
                'base_url': base_url,
                'message': 'Ollama is running and accessible'
            }
        else:
            return {
                'status': 'error',
                'available': False,
                'models': [],
                'model_count': 0,
                'base_url': base_url,
                'message': f'Ollama responded with status {response.status_code}'
            }
            
    except requests.exceptions.ConnectionError:
        return {
            'status': 'connection_error',
            'available': False,
            'models': [],
            'model_count': 0,
            'base_url': base_url,
            'message': 'Cannot connect to Ollama. Make sure it is running.'
        }
    except requests.exceptions.Timeout:
        return {
            'status': 'timeout',
            'available': False,
            'models': [],
            'model_count': 0,
            'base_url': base_url,
            'message': 'Connection to Ollama timed out'
        }
    except Exception as e:
        return {
            'status': 'error',
            'available': False,
            'models': [],
            'model_count': 0,
            'base_url': base_url,
            'message': f'Error connecting to Ollama: {str(e)}'
        }


# Convenience functions for easy integration
def quick_generate_insights(customer_data: dict, model: str = "llama3.2") -> Tuple[str, Optional[str]]:
    """Quick function to generate insights with minimal setup"""
    
    try:
        # Convert dict to CustomerInsightRequest if needed
        if isinstance(customer_data, dict):
            customer_request = CustomerInsightRequest(**customer_data)
        else:
            customer_request = customer_data
        
        config = OllamaConfig(model=model)
        insights, debug_info = generate_ollama_insights(customer_request, config)
        
        return insights, None
        
    except Exception as e:
        return None, str(e)


def is_ollama_available() -> bool:
    """Simple check if Ollama is available"""
    return check_ollama_status()


# Default models for different use cases
RECOMMENDED_MODELS = {
    'fast': 'llama3.2',          # Fast and efficient
    'quality': 'llama3.1',       # Higher quality, slower
    'balanced': 'llama3.2',      # Good balance
    'reasoning': 'phi3',         # Good for analytical tasks
    'efficient': 'mistral'       # Fast and lightweight
}


def get_recommended_model(use_case: str = 'balanced') -> str:
    """Get recommended model for specific use case"""
    return RECOMMENDED_MODELS.get(use_case, 'llama3.2')