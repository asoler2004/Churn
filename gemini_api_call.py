#!/usr/bin/env python3
"""
Gemini API Integration for Fintech Churn Prediction

This module provides AI-powered customer retention insights using Google's Gemini API.
It works independently of other AI methods and provides comprehensive customer analysis.
"""

import os
import json
import requests
from typing import Dict, Any, Tuple, Optional, List
from dataclasses import dataclass
from datetime import datetime
import time

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

print(GEMINI_AVAILABLE)

@dataclass
class GeminiConfig:
    """Configuration for Gemini API calls"""
    api_key: str = ""
    model: str = "gemini-2.5-flash"  # Default to available model
    temperature: float = 0.7
    max_output_tokens: int = 2048
    top_p: float = 0.9
    top_k: int = 40
    timeout: int = 30

@dataclass
class CustomerData:
    """Customer data structure for insights generation"""
    # Demographics
    age: int
    housing: str
    payment_type: str
    
    # Financial Profile
    credit_score: float
    deposits: int
    withdrawal: int
    purchases: int
    purchases_partners: int
    registered_phones: int
    rewards_earned: int
    reward_rate: float
    
    # Digital Engagement
    app_downloaded: int
    web_user: int
    app_web_user: int
    ios_user: int
    android_user: int
    
    # Credit Products
    cc_taken: int
    cc_recommended: int
    cc_disliked: int
    cc_liked: int
    cc_application_begin: int
    
    # Loan Activity
    waiting_4_loan: int
    cancelled_loan: int
    received_loan: int
    rejected_loan: int
    
    # Behavioral Patterns
    left_for_two_month_plus: int
    left_for_one_month: int
    is_referred: int
    
    # Prediction Results
    churn_probability: float
    churn_prediction: int
    risk_level: str

def get_api_key() -> Optional[str]:
    """Get Gemini API key from environment or config"""
    # Try environment variable first
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("---------API KEY Found----------")
        return api_key
    
    # Try config file
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('GEMINI_API_KEY='):
                    return line.split('=', 1)[1].strip().strip('"\'')
    except FileNotFoundError:
        pass
    
    # Try gemini_config.json
    try:
        with open('gemini_config.json', 'r') as f:
            config = json.load(f)
            return config.get('api_key')
    except FileNotFoundError:
        pass
    
    return None

def setup_gemini_client(api_key: str) -> bool:
    """Setup Gemini client with API key"""
    if not GEMINI_AVAILABLE:
        return False
    
    try:
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        print(f"Error setting up Gemini client: {e}")
        return False

def create_comprehensive_customer_profile(customer: CustomerData) -> str:
    """Create a detailed customer profile with all available information"""
    
    # Demographics analysis
    age_group = "Joven (18-30)" if customer.age <= 30 else "Adulto (31-50)" if customer.age <= 50 else "Maduro (50+)"
    
    housing_text = {
        "o": "Vivienda propia",
        "r": "Vivienda alquilada", 
        "na": "Situación de vivienda no especificada"
    }.get(customer.housing, customer.housing)
    
    payment_text = {
        "monthly": "Pagos mensuales",
        "bi-weekly": "Pagos quincenales", 
        "weekly": "Pagos semanales",
        "semi-monthly": "Pagos bimensuales",
        "na": "Tipo de pago no especificado"
    }.get(customer.payment_type, customer.payment_type)
    
    # Financial health analysis
    credit_tier = "Excelente (750+)" if customer.credit_score >= 750 else \
                  "Bueno (650-749)" if customer.credit_score >= 650 else \
                  "Regular (550-649)" if customer.credit_score >= 550 else \
                  "Bajo (<550)"
    
    # Activity analysis
    total_transactions = customer.deposits + customer.withdrawal + customer.purchases + customer.purchases_partners
    activity_level = "Muy Alta (40+)" if total_transactions >= 40 else \
                     "Alta (25-39)" if total_transactions >= 25 else \
                     "Media (15-24)" if total_transactions >= 15 else \
                     "Baja (<15)"
    
    # Digital engagement score
    digital_channels = customer.app_downloaded + customer.web_user + customer.ios_user + customer.android_user
    digital_adoption = "Completa (3-4 canales)" if digital_channels >= 3 else \
                       "Parcial (1-2 canales)" if digital_channels >= 1 else \
                       "Limitada (0 canales)"
    
    # Product portfolio
    products_held = customer.cc_taken + customer.received_loan
    product_engagement = "Multi-producto" if products_held >= 2 else \
                        "Un producto" if products_held == 1 else \
                        "Sin productos principales"
    
    # Risk indicators
    risk_factors = []
    if customer.left_for_one_month:
        risk_factors.append("Inactivo por 1 mes")
    if customer.left_for_two_month_plus:
        risk_factors.append("Inactivo por 2+ meses")
    if customer.cancelled_loan:
        risk_factors.append("Préstamo cancelado")
    if customer.rejected_loan:
        risk_factors.append("Préstamo rechazado")
    if customer.cc_disliked:
        risk_factors.append("Sentimiento negativo hacia tarjeta de crédito")
    if not customer.app_downloaded:
        risk_factors.append("No ha descargado la app móvil")
    if customer.purchases < 10:
        risk_factors.append("Baja actividad de compras")
    if customer.rewards_earned < 50:
        risk_factors.append("Bajo engagement con programa de recompensas")
    
    # Opportunities
    opportunities = []
    if not customer.app_downloaded:
        opportunities.append("Adopción de aplicación móvil")
    if not customer.cc_taken and customer.credit_score > 650:
        opportunities.append("Oferta de tarjeta de crédito")
    if customer.waiting_4_loan:
        opportunities.append("Procesamiento prioritario de préstamo pendiente")
    if customer.rewards_earned < 100 and customer.purchases > 15:
        opportunities.append("Activación mejorada del programa de recompensas")
    if customer.is_referred:
        opportunities.append("Aprovechamiento de red de referidos")
    if customer.cc_liked and not customer.cc_taken:
        opportunities.append("Conversión de interés en tarjeta de crédito")
    if customer.web_user and not customer.app_downloaded:
        opportunities.append("Migración de web a app móvil")
    
    # Behavioral patterns
    engagement_pattern = "Alto compromiso" if customer.rewards_earned > 200 and total_transactions > 25 else \
                        "Compromiso moderado" if customer.rewards_earned > 50 and total_transactions > 10 else \
                        "Bajo compromiso"
    
    channel_preference = "Digital nativo" if digital_channels >= 2 else \
                        "Adopción digital parcial" if digital_channels == 1 else \
                        "Preferencia tradicional"
    
    credit_relationship = "Positiva" if customer.cc_liked or customer.received_loan else \
                         "Negativa" if customer.cc_disliked or customer.rejected_loan else \
                         "Neutral"
    
    profile = f"""
PERFIL DEMOGRÁFICO Y SOCIOECONÓMICO:
• Edad: {customer.age} años ({age_group})
• Situación de vivienda: {housing_text}
• Patrón de pagos: {payment_text}
• Puntaje crediticio: {customer.credit_score:.0f}/850 ({credit_tier})

ACTIVIDAD FINANCIERA Y TRANSACCIONAL:
• Nivel de actividad general: {activity_level} ({total_transactions} transacciones totales)
• Depósitos realizados: {customer.deposits} operaciones
• Retiros realizados: {customer.withdrawal} operaciones
• Compras directas: {customer.purchases} transacciones
• Compras con socios comerciales: {customer.purchases_partners} transacciones
• Dispositivos registrados: {customer.registered_phones} teléfono(s)
• Ratio actividad depósitos/retiros: {customer.deposits/max(customer.withdrawal, 1):.2f}

PORTAFOLIO DE PRODUCTOS Y SERVICIOS:
• Engagement de productos: {product_engagement}
• Tarjeta de crédito: {'Activa' if customer.cc_taken else 'No tomada'}
• Historial de recomendación TC: {'Recibió recomendación' if customer.cc_recommended else 'Sin recomendación'}
• Sentimiento hacia TC: {'Positivo' if customer.cc_liked else 'Negativo' if customer.cc_disliked else 'Neutral'}
• Proceso de aplicación TC: {'Iniciado' if customer.cc_application_begin else 'No iniciado'}
• Estado de préstamos: {'Activo' if customer.received_loan else 'Rechazado' if customer.rejected_loan else 'En espera' if customer.waiting_4_loan else 'Cancelado' if customer.cancelled_loan else 'Sin actividad'}

ADOPCIÓN Y ENGAGEMENT DIGITAL:
• Nivel de adopción digital: {digital_adoption}
• Aplicación móvil: {'Descargada y activa' if customer.app_downloaded else 'No descargada'}
• Usuario web: {'Activo' if customer.web_user else 'Inactivo'}
• Usuario multiplataforma: {'Sí (app+web)' if customer.app_web_user else 'No'}
• Plataforma iOS: {'Usuario activo' if customer.ios_user else 'No usuario'}
• Plataforma Android: {'Usuario activo' if customer.android_user else 'No usuario'}
• Preferencia de canal: {channel_preference}

PROGRAMA DE RECOMPENSAS Y FIDELIZACIÓN:
• Puntos acumulados: {customer.rewards_earned} puntos
• Tasa de recompensa: {customer.reward_rate:.3f} ({customer.reward_rate*100:.1f}%)
• Nivel de engagement: {engagement_pattern}
• Cliente referido: {'Sí, llegó por referencia' if customer.is_referred else 'No, adquisición directa'}

PATRONES DE COMPORTAMIENTO Y RIESGO:
• Relación con productos de crédito: {credit_relationship}
• Patrón de actividad reciente: {'Inactivo 2+ meses' if customer.left_for_two_month_plus else 'Inactivo 1 mes' if customer.left_for_one_month else 'Activo'}
• Frecuencia de uso: {'Alta' if total_transactions > 25 else 'Media' if total_transactions > 10 else 'Baja'}
• Nivel de compromiso general: {engagement_pattern}

INDICADORES DE RIESGO IDENTIFICADOS:
{chr(10).join(f'• {factor}' for factor in risk_factors) if risk_factors else '• No se identificaron factores de riesgo críticos'}

OPORTUNIDADES DE CRECIMIENTO:
{chr(10).join(f'• {opportunity}' for opportunity in opportunities) if opportunities else '• Cliente con perfil estable, enfocarse en retención y satisfacción'}

MÉTRICAS CLAVE DE RENDIMIENTO:
• Valor transaccional promedio: {(customer.purchases + customer.purchases_partners)/max(total_transactions, 1):.2f}
• Ratio de adopción digital: {digital_channels}/4 ({digital_channels/4*100:.0f}%)
• Índice de diversificación de productos: {products_held}/2 ({products_held/2*100:.0f}%)
• Score de engagement de recompensas: {min(customer.rewards_earned/500, 1)*100:.0f}%
• Indicador de estabilidad financiera: {min(customer.credit_score/850, 1)*100:.0f}%
"""
    
    return profile

def create_enhanced_prompt(customer: CustomerData) -> str:
    """Create a minimal, safe prompt for Gemini"""
    
    # Create a very simple, positive customer summary
    total_transactions = customer.deposits + customer.withdrawal + customer.purchases + customer.purchases_partners
    
    prompt = f"""You are a customer success consultant. A fintech customer has this profile:

- Age: {customer.age} years
- Credit score: {customer.credit_score:.0f}
- Monthly activity: {total_transactions} transactions
- Mobile app: {'Yes' if customer.app_downloaded else 'No'}
- Rewards earned: {customer.rewards_earned} points

Please provide 5 brief recommendations in Spanish to improve this customer's experience and engagement with the platform. Focus on positive actions and service improvements."""

    return prompt

def generate_gemini_insights(customer_data: Dict[str, Any], config: Optional[GeminiConfig] = None) -> Tuple[str, Optional[Dict]]:
    """Generate customer insights using Gemini API with simplified approach"""
    
    if not GEMINI_AVAILABLE:
        raise Exception("Google Generative AI library not available. Install with: pip install google-generativeai")
    
    # Get API key
    api_key = config.api_key if config and config.api_key else get_api_key()
    if not api_key:
        raise Exception("Gemini API key not found. Set GEMINI_API_KEY environment variable or create gemini_config.json")
    
    # Setup client
    if not setup_gemini_client(api_key):
        raise Exception("Failed to setup Gemini client")
    
    # Use default config if none provided
    if config is None:
        config = GeminiConfig(api_key=api_key)
    
    try:
        # Extract key customer metrics safely
        age = customer_data.get('age', 30)
        credit_score = customer_data.get('credit_score', 650)
        total_transactions = (customer_data.get('deposits', 0) + 
                            customer_data.get('withdrawal', 0) + 
                            customer_data.get('purchases', 0) + 
                            customer_data.get('purchases_partners', 0))
        app_downloaded = customer_data.get('app_downloaded', 0)
        rewards_earned = customer_data.get('rewards_earned', 0)
        churn_probability = customer_data.get('churn_probability', 0)
        risk_level = customer_data.get('risk_level', 'Medium')
        
        # Create very simple, safe prompt
        prompt = f"""You are a customer success consultant. A customer has this profile:

- Age: {age} years
- Credit score: {credit_score:.0f}
- Monthly activity: {total_transactions} transactions
- Mobile app: {'Yes' if app_downloaded else 'No'}
- Rewards: {rewards_earned} points

Please provide 5 brief recommendations in Spanish to improve this customer's experience with the financial platform. Focus on positive service improvements and engagement strategies."""

        # Configure safety settings
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_ONLY_HIGH"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_ONLY_HIGH"
            }
        ]
        
        # Configure generation parameters
        generation_config = genai.types.GenerationConfig(
            temperature=config.temperature,
            max_output_tokens=config.max_output_tokens,
            top_p=config.top_p,
            top_k=config.top_k,
        )
        
        # Initialize model
        model = genai.GenerativeModel(
            model_name=config.model,
            generation_config=generation_config,
            safety_settings=safety_settings
        )
        
        # Generate response
        start_time = time.time()
        response = model.generate_content(prompt)
        generation_time = time.time() - start_time
        
        # Check if response has text
        if not hasattr(response, 'text') or not response.text:
            raise Exception("🛡️ Respuesta bloqueada por filtros de seguridad de Gemini. Intenta con datos diferentes o contacta soporte.")
        
        response_text = response.text
        
        # Format the response
        formatted_response = f"""
INSIGHTS GENERADOS POR GEMINI ({config.model}):

{response_text}

RESUMEN EJECUTIVO:
• Nivel de engagement: {risk_level}
• Probabilidad de satisfacción: {(1-churn_probability)*100:.1f}%
• Tiempo de generación: {generation_time:.2f} segundos
• Modelo utilizado: {config.model}

PRÓXIMOS PASOS:
1. Implementar recomendaciones prioritarias
2. Configurar monitoreo de métricas clave
3. Programar seguimiento personalizado
4. Evaluar efectividad de intervenciones
"""
        
        # Prepare debug information
        debug_info = {
            'prompt': prompt,
            'raw_response': response_text,
            'model_used': config.model,
            'generation_time': generation_time,
            'config': {
                'temperature': config.temperature,
                'max_output_tokens': config.max_output_tokens,
                'top_p': config.top_p,
                'top_k': config.top_k
            }
        }
        
        return formatted_response, debug_info
        
    except Exception as e:
        raise Exception(f"Error generating Gemini insights: {str(e)}")

def quick_gemini_insights(customer_data: Dict[str, Any], model: str = "gemini-2.5-flash") -> Tuple[Optional[str], Optional[str]]:
    """Quick function to generate insights with minimal setup"""
    
    try:
        config = GeminiConfig(model=model)
        insights, debug_info = generate_gemini_insights(customer_data, config)
        return insights, None
    except Exception as e:
        return None, str(e)

def test_gemini_connection() -> Dict[str, Any]:
    """Test Gemini API connection and return status"""
    
    if not GEMINI_AVAILABLE:
        return {
            'available': False,
            'status': 'library_missing',
            'message': 'Google Generative AI library not installed',
            'models': []
        }
    
    api_key = get_api_key()
    if not api_key:
        return {
            'available': False,
            'status': 'no_api_key',
            'message': 'Gemini API key not found',
            'models': []
        }
    
    try:
        # Setup client
        genai.configure(api_key=api_key)
        
        # Test with a simple request using available model
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content("Test connection. Respond with 'OK'.")
        
        if response.text:
            return {
                'available': True,
                'status': 'connected',
                'message': 'Gemini API is accessible and working',
                'models': ['gemini-2.5-flash', 'gemini-1.5-pro', 'gemini-1.0-pro'],
                'test_response': response.text.strip()
            }
        else:
            return {
                'available': False,
                'status': 'empty_response',
                'message': 'Gemini API connected but returned empty response',
                'models': []
            }
            
    except Exception as e:
        return {
            'available': False,
            'status': 'connection_error',
            'message': f'Error connecting to Gemini API: {str(e)}',
            'models': []
        }

def create_config_file(api_key: str) -> bool:
    """Create a configuration file for Gemini API"""
    
    config = {
        "api_key": api_key,
        "default_model": "gemini-2.5-flash",
        "default_temperature": 0.7,
        "default_max_tokens": 2048,
        "created_at": datetime.now().isoformat()
    }
    
    try:
        with open('gemini_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        print(f"Error creating config file: {e}")
        return False

# Available models for different use cases
GEMINI_MODELS = {
    'fast': 'gemini-2.5-flash',           # Fast and efficient
    'quality': 'gemini-2.5-flash',        # Higher quality
    'balanced': 'gemini-2.5-flash',       # Good balance (default)
    'legacy': 'gemini-2.5-flash'          # Available model
}

def get_recommended_model(use_case: str = 'balanced') -> str:
    """Get recommended Gemini model for specific use case"""
    return GEMINI_MODELS.get(use_case, 'gemini-2.5-flash')

# Convenience functions
def is_gemini_available() -> bool:
    """Check if Gemini is available and configured"""
    if not GEMINI_AVAILABLE:
        return False
    
    api_key = get_api_key()
    return api_key is not None

def get_available_models() -> List[str]:
    """Get list of available Gemini models"""
    try:
        # Try to get models from API
        api_key = get_api_key()
        if api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=api_key)
            models = genai.list_models()
            model_names = []
            for model in models:
                if 'generateContent' in model.supported_generation_methods:
                    # Extract model name from full path
                    model_name = model.name.split('/')[-1] if '/' in model.name else model.name
                    model_names.append(model_name)
            
            if model_names:
                return model_names
    except Exception as e:
        print(f"Could not fetch models from API: {e}")
    
    # Fallback to known working models
    return ['gemini-2.5-flash', 'gemini-pro-vision']

if __name__ == "__main__":
    # Simple test when run directly
    print("🤖 Gemini API Integration Test")
    print("=" * 40)
    
    status = test_gemini_connection()
    print(f"Status: {status['status']}")
    print(f"Available: {status['available']}")
    print(f"Message: {status['message']}")
    
    if status['available']:
        print("✅ Gemini API is ready for use!")
    else:
        print("❌ Gemini API setup needed")
        print("\nSetup instructions:")
        print("1. Get API key from https://makersuite.google.com/app/apikey")
        print("2. Set environment variable: export GEMINI_API_KEY='your-key'")
        print("3. Or create gemini_config.json with your API key")