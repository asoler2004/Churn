from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any, Optional, Tuple
import json
import os
import requests
import asyncio

# Import the dedicated Ollama module
from ollama_local import (
    generate_ollama_insights as ollama_generate_insights,
    check_ollama_status,
    get_available_models,
    test_ollama_connection,
    CustomerInsightRequest as OllamaCustomerRequest,
    OllamaConfig,
    quick_generate_insights,
    is_ollama_available,
    get_recommended_model
)

# Initialize the LLM model
generator = None
model_loaded = False

def initialize_llm_model():
    """Initialize the LLM model with error handling"""
    global generator, model_loaded
    
    try:
        # Try different models in order of preference
        model_options = [            
            "distilgpt2",  # Even smaller fallback
            "gpt2",  # Fallback to GPT-2            
            "microsoft/DialoGPT-small",  # Smaller, faster model
            # "microsoft/Phi-3-mini-4k-instruct",
        ]
        
        for model_name in model_options:
            try:
                print(f"Attempting to load model: {model_name}")
                
                # Load tokenizer and model
                tokenizer = AutoTokenizer.from_pretrained(model_name)
                model = AutoModelForCausalLM.from_pretrained(model_name)
                
                # Add padding token if it doesn't exist
                if tokenizer.pad_token is None:
                    tokenizer.pad_token = tokenizer.eos_token
                
                # Create text generation pipeline
                generator = pipeline(
                    "text-generation",
                    model=model,
                    tokenizer=tokenizer,
                    max_length=300,  # Reduced for faster generation
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=tokenizer.eos_token_id,
                    device=-1  # Use CPU to avoid GPU memory issues
                )
                
                print(f"LLM model '{model_name}' loaded successfully!")
                model_loaded = True
                return True
                
            except Exception as model_error:
                print(f"Failed to load {model_name}: {model_error}")
                continue
        
        print("All model loading attempts failed")
        return False
        
    except Exception as e:
        print(f"Error in model initialization: {e}")
        return False

# Try to initialize the model
initialize_llm_model()

app = FastAPI(title="API LLM de Retención de Clientes", version="1.0.0")

class CustomerInsightRequest(BaseModel):
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
    use_transformers: Optional[bool] = False
    use_ollama: Optional[bool] = False  # New field for Ollama support
    ollama_model: Optional[str] = "llama3.2"  # Default Ollama model

class InsightResponse(BaseModel):
    recommendations: str
    key_insights: str
    action_items: str
    debug_prompt: Optional[str] = None
    debug_raw_response: Optional[str] = None

def generate_customer_insights(customer_data: CustomerInsightRequest) -> Tuple[str, Optional[Dict]]:
    """Generate actionable insights for customer retention"""
    
    # Priority order: Ollama > Transformers > Rule-based
    if customer_data.use_ollama:
        try:
            insights, debug_info = generate_ollama_insights(customer_data)
            return insights, debug_info
        except Exception as e:
            print(f"Ollama generation failed: {e}, falling back to transformers or rule-based")
            # Fall back to transformers if available, otherwise rule-based
            if customer_data.use_transformers and model_loaded and generator is not None:
                try:
                    insights, debug_info = generate_transformers_insights(customer_data)
                    return insights, debug_info
                except Exception as e2:
                    print(f"Transformers also failed: {e2}, using rule-based")
                    return generate_rule_based_insights(customer_data), None
            else:
                return generate_rule_based_insights(customer_data), None
    
    # Check if transformers should be used and if model is available
    elif customer_data.use_transformers and model_loaded and generator is not None:
        try:
            insights, debug_info = generate_transformers_insights(customer_data)
            return insights, debug_info
        except Exception as e:
            print(f"Transformers generation failed: {e}, falling back to rule-based")
            # Fall back to rule-based if transformers fails
            return generate_rule_based_insights(customer_data), None
    else:
        # Use rule-based approach
        return generate_rule_based_insights(customer_data), None

def generate_ollama_insights(customer_data: CustomerInsightRequest) -> Tuple[str, Dict]:
    """Generate insights using Ollama local LLM via the dedicated module"""
    
    try:
        # Convert to OllamaCustomerRequest format
        ollama_data = OllamaCustomerRequest(
            age=customer_data.age,
            housing=customer_data.housing,
            credit_score=customer_data.credit_score,
            deposits=customer_data.deposits,
            withdrawal=customer_data.withdrawal,
            purchases_partners=customer_data.purchases_partners,
            purchases=customer_data.purchases,
            cc_taken=customer_data.cc_taken,
            cc_recommended=customer_data.cc_recommended,
            cc_disliked=customer_data.cc_disliked,
            cc_liked=customer_data.cc_liked,
            cc_application_begin=customer_data.cc_application_begin,
            app_downloaded=customer_data.app_downloaded,
            web_user=customer_data.web_user,
            app_web_user=customer_data.app_web_user,
            ios_user=customer_data.ios_user,
            android_user=customer_data.android_user,
            registered_phones=customer_data.registered_phones,
            payment_type=customer_data.payment_type,
            waiting_4_loan=customer_data.waiting_4_loan,
            cancelled_loan=customer_data.cancelled_loan,
            received_loan=customer_data.received_loan,
            rejected_loan=customer_data.rejected_loan,
            left_for_two_month_plus=customer_data.left_for_two_month_plus,
            left_for_one_month=customer_data.left_for_one_month,
            rewards_earned=customer_data.rewards_earned,
            reward_rate=customer_data.reward_rate,
            is_referred=customer_data.is_referred,
            churn_probability=customer_data.churn_probability,
            churn_prediction=customer_data.churn_prediction,
            risk_level=customer_data.risk_level
        )
        
        # Create Ollama configuration
        config = OllamaConfig(
            model=customer_data.ollama_model,
            temperature=0.7,
            top_p=0.9,
            max_tokens=1000,
            timeout=60
        )
        
        # Use the dedicated Ollama module
        return ollama_generate_insights(ollama_data, config)
        
    except Exception as e:
        raise Exception(f"Error en generación Ollama: {str(e)}")

# Customer profiling is now handled by the ollama_local module
# create_comprehensive_customer_profile is available from ollama_local import

def generate_transformers_insights(customer_data: CustomerInsightRequest) -> Tuple[str, Dict]:
    """Generate insights using transformers pipeline"""
    
    # Use the same comprehensive customer profile as Ollama for consistency
    customer_profile = create_comprehensive_customer_profile(customer_data)
    
    # Create an enhanced but concise prompt for transformers (they have token limitations)
    prompt = f"""Analista fintech: Cliente {customer_data.age} años, score {customer_data.credit_score:.0f}, riesgo {str(customer_data.risk_level).lower()} ({customer_data.churn_probability:.1%}).

PERFIL CLAVE:
• Actividad: {customer_data.purchases} compras, {customer_data.deposits} depósitos
• Digital: {'App activa' if customer_data.app_downloaded else 'Sin app'}, {'Web activo' if customer_data.web_user else 'Sin web'}
• Productos: {'TC activa' if customer_data.cc_taken else 'Sin TC'}, {'Préstamo activo' if customer_data.received_loan else 'Sin préstamo'}
• Recompensas: {customer_data.rewards_earned} puntos ganados
• Riesgos: {'Inactivo 1+ mes' if customer_data.left_for_one_month or customer_data.left_for_two_month_plus else 'Activo'}

ESTRATEGIA DE RETENCIÓN:
1."""
    
    try:
        # Generate response using the transformers pipeline with more randomization
        import random
        
        # Add randomization to temperature and other parameters for more varied responses
        temperature = random.uniform(0.6, 0.9)  # Vary temperature for different responses
        top_p = random.uniform(0.85, 0.95)  # Add nucleus sampling variation
        
        response = generator(
            prompt,
            max_new_tokens=100,  # Reduced for better generation
            min_length=len(prompt.split()) + 20,  # Ensure some new content
            num_return_sequences=1,
            temperature=0.8,  # Fixed temperature for more creativity
            top_p=0.9,  # Fixed top_p
            do_sample=True,
            pad_token_id=generator.tokenizer.eos_token_id,
            repetition_penalty=1.2,  # Higher penalty to avoid repetition
            no_repeat_ngram_size=3,  # Prevent 3-gram repetition
            early_stopping=True,
            truncation=True
        )
        
        # Extract the generated text
        generated_text = response[0]['generated_text']
        raw_response = generated_text  # Store the complete raw response
        
        # Remove the original prompt from the response
        insights_text = generated_text.replace(prompt, "").strip()
        
        # If the generated text is too short or empty, enhance it
        if len(insights_text) < 50:
            insights_text = enhance_short_response(customer_data, insights_text)
        
        # Format the response properly
        formatted_response = f"""
INSIGHTS GENERADOS POR IA:

{insights_text}

ANÁLISIS AUTOMÁTICO:
• Riesgo de abandono: {customer_data.risk_level} ({customer_data.churn_probability:.1%})
• Prioridad de intervención: {'Alta' if customer_data.risk_level == 'High' else 'Media' if customer_data.risk_level == 'Medium' else 'Baja'}
• Perfil del cliente: {get_customer_profile_summary(customer_data)}

PRÓXIMOS PASOS SUGERIDOS:
1. Implementar recomendaciones principales dentro de 48 horas
2. Monitorear engagement del cliente semanalmente  
3. Evaluar efectividad de las acciones en 30 días
4. Ajustar estrategia basada en respuesta del cliente
"""
        
        # Prepare debug information
        debug_info = {
            'prompt': prompt,
            'raw_response': raw_response,
            'insights_text_extracted': insights_text,
            'model_parameters': {
                'temperature': temperature,
                'top_p': top_p,
                'max_length': len(prompt.split()) + 200,
                'repetition_penalty': 1.1
            }
        }
        
        return formatted_response, debug_info
        
    except Exception as e:
        print(f"Error in transformers generation: {e}")
        # Fall back to a hybrid approach
        fallback_response = generate_hybrid_insights(customer_data, str(e))
        
        # Create debug info for the error case
        debug_info = {
            'prompt': prompt if 'prompt' in locals() else "Prompt not available",
            'raw_response': f"ERROR: {str(e)}",
            'insights_text_extracted': "Error occurred during generation",
            'error': str(e),
            'fallback_used': True
        }
        
        return fallback_response, debug_info

def enhance_short_response(customer_data: CustomerInsightRequest, short_text: str) -> str:
    """Enhance short AI responses with structured recommendations"""
    
    enhancements = []
    
    if customer_data.risk_level == "High":
        enhancements.append("• Contacto inmediato requerido - llamada personal dentro de 24 horas")
        enhancements.append("• Ofrecer soporte premium o asignación de gerente de cuenta")
    
    if not customer_data.app_downloaded:
        enhancements.append("• Promover descarga de app móvil con incentivos especiales")
    
    if customer_data.credit_score > 750:
        enhancements.append("• Ofrecer productos premium y servicios de inversión exclusivos")
    elif customer_data.credit_score < 600:
        enhancements.append("• Proporcionar recursos de mejora crediticia y educación financiera")
    
    if customer_data.left_for_one_month or customer_data.left_for_two_month_plus:
        enhancements.append("• Implementar campaña de reconquista con ofertas personalizadas")
    
    enhanced_text = short_text
    if enhancements:
        enhanced_text += "\n\nRECOMENDACIONES ADICIONALES:\n" + "\n".join(enhancements)
    
    return enhanced_text

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

def generate_hybrid_insights(customer_data: CustomerInsightRequest, error_msg: str) -> str:
    """Generate insights using a hybrid approach when transformers fail"""
    
    rule_based = generate_rule_based_insights(customer_data)
    
    hybrid_response = f"""
INSIGHTS HÍBRIDOS (IA + Reglas):

NOTA: Generación de IA no disponible ({error_msg[:50]}...), usando análisis híbrido.

{rule_based}

ANÁLISIS MEJORADO:
• Modelo de IA: Temporalmente no disponible
• Análisis de reglas: Completado exitosamente
• Confiabilidad: Alta (basado en patrones establecidos)
• Recomendación: Implementar acciones sugeridas con monitoreo continuo
"""
    
    return hybrid_response

def generate_rule_based_insights(customer_data: CustomerInsightRequest) -> str:
    """Generate insights using rule-based approach in Spanish"""
    
    recommendations = []
    key_insights = []
    action_items = []
    
    # Risk level analysis
    if customer_data.risk_level == "High":
        recommendations.append("🚨 ALTA PRIORIDAD: Se requiere intervención inmediata")
        action_items.append("Programar llamada personal dentro de 24 horas")
        action_items.append("Ofrecer soporte premium o gerente de cuenta")
    elif customer_data.risk_level == "Medium":
        recommendations.append("⚠️ PRIORIDAD MEDIA: Se necesita compromiso proactivo")
        action_items.append("Enviar oferta de retención personalizada")
    else:
        recommendations.append("✅ RIESGO BAJO: Enfocarse en compromiso y satisfacción")
    
    # Digital engagement analysis
    if not customer_data.app_downloaded:
        recommendations.append("📱 Fomentar adopción de app móvil con incentivos")
        action_items.append("Enviar oferta de bonificación por descarga de app")
    
    if customer_data.left_for_one_month or customer_data.left_for_two_month_plus:
        key_insights.append("El cliente muestra patrones de inactividad - re-compromiso crítico")
        recommendations.append("🔄 Implementar campaña de reconquista")
        action_items.append("Enviar email 'Te extrañamos' con ofertas especiales")
    
    # Credit score and financial health
    if customer_data.credit_score < 600:
        recommendations.append("💳 Ofrecer recursos y herramientas de mejora crediticia")
        action_items.append("Proporcionar contenido de bienestar financiero")
    elif customer_data.credit_score > 750:
        recommendations.append("⭐ Ofrecer productos y servicios premium")
        action_items.append("Presentar oportunidades de inversión exclusivas")
    
    # Banking activity analysis
    if customer_data.deposits < 3:
        key_insights.append("Baja actividad de depósitos indica compromiso limitado")
        recommendations.append("💰 Fomentar configuración de depósito directo con incentivos")
        action_items.append("Ofrecer bonificación por depósito directo")
    
    if customer_data.purchases < 10:
        recommendations.append("🛒 Promover recompensas de gastos y programas de cashback")
        action_items.append("Enviar ofertas de comerciantes dirigidas")
    
    # Credit card engagement
    if customer_data.cc_disliked:
        key_insights.append("El cliente tiene sentimiento negativo hacia productos de crédito")
        recommendations.append("🤝 Enfocarse en construir confianza a través de educación")
        action_items.append("Compartir contenido educativo sobre crédito")
    elif not customer_data.cc_taken and customer_data.credit_score > 650:
        recommendations.append("💳 Presentar ofertas de tarjeta de crédito personalizadas")
        action_items.append("Enviar invitación de tarjeta de crédito pre-aprobada")
    
    # Loan activity insights
    if customer_data.rejected_loan:
        key_insights.append("Rechazo previo de préstamo puede indicar frustración")
        recommendations.append("🏦 Ofrecer productos de préstamo alternativos o asesoría financiera")
        action_items.append("Proporcionar consejos de mejora de préstamos")
    elif customer_data.received_loan:
        key_insights.append("Cliente exitoso de préstamo - relación de alto valor")
        recommendations.append("🎯 Venta cruzada de productos financieros adicionales")
    
    # Rewards and referral analysis
    if customer_data.rewards_earned < 50:
        recommendations.append("🎁 Educar sobre beneficios del programa de recompensas")
        action_items.append("Enviar tutorial del programa de recompensas")
    elif customer_data.rewards_earned > 500:
        key_insights.append("Alto ganador de recompensas - cliente comprometido")
        recommendations.append("🏆 Ofrecer estatus VIP o beneficios exclusivos")
    
    if customer_data.is_referred:
        key_insights.append("Cliente referido - probablemente mayor valor de por vida")
        recommendations.append("👥 Aprovechar red de referidos para retención")
    
    # Age-based recommendations
    if customer_data.age < 30:
        recommendations.append("🎓 Ofrecer productos financieros para estudiantes/jóvenes profesionales")
        action_items.append("Presentar herramientas de presupuesto y ahorro")
    elif customer_data.age > 50:
        recommendations.append("🏡 Enfocarse en planificación de jubilación e inversiones")
        action_items.append("Programar consulta de planificación financiera")
    
    # NEW ENHANCED RULES
    
    # Rule 1: Young customers with low credit score and medium-high churn risk
    if (customer_data.age < 30 and customer_data.credit_score < 600 and 
        customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Cliente joven con score crediticio bajo - oportunidad de desarrollo financiero")
        recommendations.append("📚 Implementar programa de educación financiera personalizado")
        recommendations.append("🔧 Ofrecer herramientas para mejorar score crediticio")
        action_items.append("Enviar guía de construcción de crédito para jóvenes")
        action_items.append("Ofrecer acceso facilitado a préstamos con condiciones educativas")
    
    # Rule 2: Senior customers (60+) with medium-high risk - digital engagement
    if (customer_data.age > 60 and customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Cliente senior con riesgo elevado - necesita mayor compromiso digital")
        recommendations.append("👨‍💻 Fomentar adopción de servicios digitales con soporte personalizado")
        recommendations.append("🎓 Ofrecer educación digital y tutoriales paso a paso")
        action_items.append("Programar sesión de entrenamiento digital personalizada")
        action_items.append("Asignar especialista en servicios digitales para seniors")
    
    # Rule 3: Very low credit score with medium-high churn risk
    if (customer_data.credit_score < 400 and customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Score crediticio crítico - requiere soporte financiero integral")
        recommendations.append("🆘 Implementar campaña de soporte financiero de emergencia")
        recommendations.append("🎯 Desarrollar productos personalizados para reconstrucción crediticia")
        action_items.append("Contactar para evaluación de situación financiera")
        action_items.append("Ofrecer plan de recuperación crediticia personalizado")
    
    # Rule 4: Low partner purchases with medium-high churn risk
    if (customer_data.purchases_partners < 3 and customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Baja actividad en compras con socios - oportunidad de incrementar transacciones")
        recommendations.append("🛍️ Activar programa de incentivos para compras con socios")
        recommendations.append("📱 Promover uso de app web con descuentos exclusivos")
        action_items.append("Enviar cupones de descuento para tiendas socias")
        action_items.append("Ofrecer cashback aumentado por compras con socios")
    
    # Rule 5: Referred customers with medium-high churn risk
    if (customer_data.is_referred and customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Cliente referido con riesgo - aprovechar conexión de referencia")
        recommendations.append("🎉 Reconocer y recompensar por haber sido referido")
        recommendations.append("👥 Incentivar programa de referidos con recompensas dobles")
        action_items.append("Enviar agradecimiento personalizado por ser cliente referido")
        action_items.append("Ofrecer bonificación por referir nuevos clientes")
    
    # Rule 6: Low churn risk + high credit score - referral opportunity
    if (customer_data.risk_level == "Low" and customer_data.credit_score > 700):
        key_insights.append("Cliente estable con excelente perfil crediticio - embajador potencial")
        recommendations.append("🌟 Activar como embajador de marca con programa VIP de referidos")
        recommendations.append("💎 Ofrecer beneficios exclusivos por referir clientes de calidad")
        action_items.append("Invitar a programa exclusivo de referidos VIP")
        action_items.append("Ofrecer descuentos premium por cada referido exitoso")
    
    # Rule 7: Weekly payment customers with medium-high churn risk
    if (customer_data.payment_type == "weekly" and customer_data.risk_level in ["Medium", "High"]):
        key_insights.append("Pagos semanales pueden indicar presión financiera")
        recommendations.append("💳 Promover modalidades de pago más flexibles")
        recommendations.append("📅 Ofrecer opciones de pago mensual o quincenal")
        action_items.append("Presentar opciones de pago que reduzcan carga financiera percibida")
        action_items.append("Evaluar elegibilidad para planes de pago extendidos")
    
    # Rule 8: Rented home + high credit score customers
    if (customer_data.housing == "r" and customer_data.credit_score > 700):
        if customer_data.waiting_4_loan == 1:
            key_insights.append("Cliente con buen crédito en casa rentada esperando préstamo")
            recommendations.append("🏠 Acelerar proceso de préstamo hipotecario")
            recommendations.append("📈 Incentivar mayor actividad en plataforma durante espera")
            action_items.append("Priorizar evaluación de solicitud de préstamo")
            action_items.append("Ofrecer beneficios por mantener actividad durante proceso")
        else:
            key_insights.append("Cliente con excelente crédito en casa rentada - oportunidad hipotecaria")
            recommendations.append("🏡 Presentar oportunidades de préstamo hipotecario")
            recommendations.append("💼 Ofrecer asesoría para compra de vivienda")
            action_items.append("Enviar información sobre préstamos hipotecarios")
            action_items.append("Programar consulta con especialista hipotecario")
    
    # Compile final response in Spanish
    response = f"""
INSIGHTS CLAVE:
{chr(10).join(f"• {insight}" for insight in key_insights) if key_insights else "• Perfil del cliente analizado para oportunidades de retención"}

RECOMENDACIONES:
{chr(10).join(f"• {rec}" for rec in recommendations)}

ACCIONES INMEDIATAS:
{chr(10).join(f"• {action}" for action in action_items)}

ESTRATEGIA DE RETENCIÓN:
Basado en el riesgo de abandono {str(customer_data.risk_level).lower()} ({customer_data.churn_probability:.1%} de probabilidad), 
enfocarse en {"intervención inmediata y soporte premium" if customer_data.risk_level == "High" 
else "compromiso proactivo y ofertas personalizadas" if customer_data.risk_level == "Medium" 
else "mantener satisfacción y aumentar compromiso"}.

PRÓXIMOS PASOS:
1. Implementar elementos de acción de mayor prioridad dentro de 48 horas
2. Monitorear métricas de compromiso del cliente semanalmente
3. Hacer seguimiento de iniciativas de retención dentro de 30 días
4. Programar revisión trimestral de la relación
"""
    
    return response

@app.get("/")
async def root():
    return {"message": "API LLM de Retención de Clientes", "status": "activo"}

# Use the dedicated Ollama module functions
# check_ollama_status is now imported from ollama_local

@app.get("/health")
async def health_check():
    # Get comprehensive Ollama status
    ollama_status = test_ollama_connection()
    ollama_available = ollama_status['available']
    
    return {
        "status": "saludable", 
        "llm_model_loaded": model_loaded,
        "transformers_available": generator is not None,
        "ollama_available": ollama_available,
        "ollama_models": ollama_status.get('models', []),
        "ollama_model_count": ollama_status.get('model_count', 0),
        "rule_based_available": True,
        "available_methods": {
            "ollama": ollama_available,
            "transformers": generator is not None,
            "rule_based": True
        },
        "ollama_status": ollama_status
    }

@app.get("/ollama/models")
async def get_ollama_models():
    """Get available Ollama models"""
    try:
        models = get_available_models()
        status = test_ollama_connection()
        
        return {
            "available": status['available'],
            "models": models,
            "model_count": len(models),
            "status": status['status'],
            "message": status['message'],
            "recommended_models": {
                "fast": get_recommended_model('fast'),
                "quality": get_recommended_model('quality'),
                "balanced": get_recommended_model('balanced'),
                "reasoning": get_recommended_model('reasoning'),
                "efficient": get_recommended_model('efficient')
            }
        }
    except Exception as e:
        return {
            "available": False,
            "models": [],
            "model_count": 0,
            "status": "error",
            "message": f"Error getting Ollama models: {str(e)}",
            "recommended_models": {}
        }

@app.post("/generate-insights", response_model=InsightResponse)
async def generate_insights(customer_data: CustomerInsightRequest):
    """Generar insights y recomendaciones de retención de clientes"""
    try:
        # Generate insights and capture debug info
        insights, debug_info = generate_customer_insights(customer_data)
        
        # Split the response into sections for better organization
        sections = insights.split('\n\n')
        
        # Extract different sections from the insights
        recommendations = insights
        key_insights = "Análisis completado exitosamente"
        action_items = "Ver recomendaciones para elementos de acción detallados"
        
        # Try to parse sections if they follow expected format
        if len(sections) >= 3:
            # Look for specific section headers
            for section in sections:
                section_upper = section.upper()
                if 'RECOMENDACIONES' in section_upper or 'RECOMMENDATIONS' in section_upper:
                    recommendations = section.strip()
                elif 'INSIGHTS' in section_upper or 'ANÁLISIS' in section_upper:
                    key_insights = section.strip()
                elif 'ACCIONES' in section_upper or 'ACTION' in section_upper:
                    action_items = section.strip()
        
        # If sections parsing didn't work well, use the full insights with smart defaults
        if recommendations == insights and len(insights) > 500:
            # For long insights, truncate recommendations and use full text as key_insights
            recommendations = insights[:300] + "... (ver insights completos)"
            key_insights = insights
            
            # Extract action items if present
            if 'ACCIONES INMEDIATAS' in insights or 'PRÓXIMOS PASOS' in insights:
                lines = insights.split('\n')
                action_lines = []
                capture = False
                for line in lines:
                    if 'ACCIONES INMEDIATAS' in line or 'PRÓXIMOS PASOS' in line:
                        capture = True
                        continue
                    elif capture and line.strip():
                        if line.startswith('•') or line.startswith('-') or line.startswith('1.'):
                            action_lines.append(line.strip())
                        elif len(action_lines) > 0 and not line.startswith(' '):
                            break
                
                if action_lines:
                    action_items = '\n'.join(action_lines[:5])  # First 5 action items
        
        return InsightResponse(
            recommendations=recommendations,
            key_insights=key_insights,
            action_items=action_items,
            debug_prompt=debug_info.get('prompt', None) if debug_info else None,
            debug_raw_response=debug_info.get('raw_response', None) if debug_info else None
        )
        
    except Exception as e:
        print(f"DEBUG: Exception in generate_insights: {str(e)}")
        print(f"DEBUG: Exception type: {type(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando insights: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)