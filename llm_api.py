from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from typing import Dict, Any, Optional
import json
import os

# Initialize the LLM model
generator = None
model_loaded = False

def initialize_llm_model():
    """Initialize the LLM model with error handling"""
    global generator, model_loaded
    
    try:
        # Try different models in order of preference
        model_options = [
            "microsoft/DialoGPT-small",  # Smaller, faster model
            "gpt2",  # Fallback to GPT-2
            "distilgpt2"  # Even smaller fallback
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
    use_transformers: Optional[bool] = False  # New optional field

class InsightResponse(BaseModel):
    recommendations: str
    key_insights: str
    action_items: str

def generate_customer_insights(customer_data: CustomerInsightRequest) -> str:
    """Generate actionable insights for customer retention"""
    
    # Check if transformers should be used and if model is available
    if customer_data.use_transformers and model_loaded and generator is not None:
        try:
            insights = generate_transformers_insights(customer_data)
            return insights
        except Exception as e:
            print(f"Transformers generation failed: {e}, falling back to rule-based")
            # Fall back to rule-based if transformers fails
            return generate_rule_based_insights(customer_data)
    else:
        # Use rule-based approach
        return generate_rule_based_insights(customer_data)

def generate_transformers_insights(customer_data: CustomerInsightRequest) -> str:
    """Generate insights using transformers pipeline"""
    
    # Create a structured prompt for the model
    prompt = f"""
Analiza este perfil de cliente fintech y genera recomendaciones de retención:

PERFIL DEL CLIENTE:
- Edad: {customer_data.age} años
- Vivienda: {customer_data.housing}
- Puntaje crediticio: {customer_data.credit_score}
- Riesgo de abandono: {customer_data.risk_level} ({customer_data.churn_probability:.1%})
- Actividad bancaria: {customer_data.deposits} depósitos, {customer_data.purchases} compras
- Uso de app: {'Sí' if customer_data.app_downloaded else 'No'}
- Tarjeta de crédito: {'Tomada' if customer_data.cc_taken else 'No tomada'}
- Préstamos: {'Recibido' if customer_data.received_loan else 'Rechazado' if customer_data.rejected_loan else 'Ninguno'}
- Inactividad: {'Sí' if customer_data.left_for_one_month or customer_data.left_for_two_month_plus else 'No'}

RECOMENDACIONES DE RETENCIÓN:
"""
    
    try:
        # Generate response using the transformers pipeline
        response = generator(
            prompt,
            max_length=len(prompt.split()) + 150,  # Limit response length
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )
        
        # Extract the generated text
        generated_text = response[0]['generated_text']
        
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
        
        return formatted_response
        
    except Exception as e:
        print(f"Error in transformers generation: {e}")
        # Fall back to a hybrid approach
        return generate_hybrid_insights(customer_data, str(e))

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
    
    # Compile final response in Spanish
    response = f"""
INSIGHTS CLAVE:
{chr(10).join(f"• {insight}" for insight in key_insights) if key_insights else "• Perfil del cliente analizado para oportunidades de retención"}

RECOMENDACIONES:
{chr(10).join(f"• {rec}" for rec in recommendations)}

ACCIONES INMEDIATAS:
{chr(10).join(f"• {action}" for action in action_items)}

ESTRATEGIA DE RETENCIÓN:
Basado en el riesgo de abandono {customer_data.risk_level.lower()} ({customer_data.churn_probability:.1%} de probabilidad), 
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

@app.get("/health")
async def health_check():
    return {
        "status": "saludable", 
        "llm_model_loaded": model_loaded,
        "transformers_available": generator is not None,
        "rule_based_available": True
    }

@app.post("/generate-insights", response_model=InsightResponse)
async def generate_insights(customer_data: CustomerInsightRequest):
    """Generar insights y recomendaciones de retención de clientes"""
    try:
        # Debug: Check the type of customer_data
        print(f"DEBUG: customer_data type: {type(customer_data)}")
        print(f"DEBUG: customer_data: {customer_data}")
        
        insights = generate_customer_insights(customer_data)
        
        # Split the response into sections
        sections = insights.split('\n\n')
        
        return InsightResponse(
            recommendations=insights,
            key_insights="Análisis completado exitosamente",
            action_items="Ver recomendaciones para elementos de acción detallados"
        )
        
    except Exception as e:
        print(f"DEBUG: Exception in generate_insights: {str(e)}")
        print(f"DEBUG: Exception type: {type(e)}")
        raise HTTPException(status_code=500, detail=f"Error generando insights: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8001)