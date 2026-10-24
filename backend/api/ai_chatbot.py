"""Respuesta de chatbot con modo IA opcional y salida JSON empresarial 5.0."""
import json
import os
from urllib import request, error

from .chatbot_engine import respond


SYSTEM_PROMPT = (
    "Eres el asistente de TutoUdec. Responde en español claro, concreto y útil. "
    "Si no sabes algo, dilo explícitamente y no inventes datos. "
    "Devuelve SOLO JSON válido con esta forma exacta: "
    "{"
    "\"answer\":string,"
    "\"follow_up_question\":string,"
    "\"unknown\":boolean,"
    "\"confidence\":number,"
    "\"intent\":string,"
    "\"suggestions\":[string],"
    "\"business_5_0\":{"
    "\"human_centered\":string,"
    "\"data_driven\":string,"
    "\"sustainable\":string,"
    "\"automation\":string,"
    "\"ethical_ai\":string"
    "}"
    "}"
)


def _local_response(message, history):
    answer, intent, suggestions = respond(message, history)
    unknown = intent == 'default'
    payload = {
        'answer': answer,
        'follow_up_question': (
            '¿Quieres que te ayude con otro tema de TutoUdec o de la UCundinamarca?'
            if not suggestions
            else suggestions[0]
        ),
        'unknown': unknown,
        'confidence': 0.35 if unknown else 0.87,
        'intent': intent,
        'suggestions': suggestions,
        'business_5_0': {
            'human_centered': 'Respuesta pensada para estudiantes/tutores y siguiente paso accionable.',
            'data_driven': 'Basada en base de conocimiento interna y reglas verificables del proyecto.',
            'sustainable': 'Promueve soporte institucional y uso responsable de recursos académicos.',
            'automation': 'Clasificación de intención + sugerencias automáticas por contexto.',
            'ethical_ai': 'Si no hay dato confiable, reconoce límite y evita inventar información.',
        },
    }
    return {
        'mode': 'rules',
        'provider': 'local',
        'payload': payload,
    }


def _ask_openai_json(message, history):
    api_key = os.getenv('OPENAI_API_KEY', '').strip()
    if not api_key:
        raise RuntimeError('OPENAI_API_KEY no configurada')

    model = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    history_lines = []
    for item in history[-8:]:
        intent = item.get('intent') if isinstance(item, dict) else None
        if intent:
            history_lines.append(f"- intent previo: {intent}")
    context = '\n'.join(history_lines) if history_lines else 'Sin contexto previo útil.'

    user_prompt = (
        f"Contexto previo:\n{context}\n\n"
        f"Mensaje usuario:\n{message}\n\n"
        "Responde en formato JSON exacto según instrucciones del sistema."
    )

    body = {
        'model': model,
        'temperature': 0.2,
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': user_prompt},
        ],
    }

    req = request.Request(
        'https://api.openai.com/v1/chat/completions',
        data=json.dumps(body).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    try:
        with request.urlopen(req, timeout=25) as resp:
            raw = json.loads(resp.read().decode('utf-8'))
    except error.HTTPError as exc:
        raise RuntimeError(f'Error HTTP proveedor IA: {exc.code}') from exc
    except error.URLError as exc:
        raise RuntimeError('No se pudo conectar con proveedor IA') from exc

    try:
        content = raw['choices'][0]['message']['content']
        payload = json.loads(content)
    except (KeyError, IndexError, json.JSONDecodeError) as exc:
        raise RuntimeError('Respuesta IA inválida; no devolvió JSON parseable') from exc

    if not isinstance(payload, dict):
        raise RuntimeError('Respuesta IA inválida; se esperaba un objeto JSON')

    payload.setdefault('suggestions', [])
    payload.setdefault('intent', 'ai_general')
    payload.setdefault('follow_up_question', '¿Quieres que profundice en un punto específico?')
    payload.setdefault('unknown', False)
    payload.setdefault('confidence', 0.75)
    payload.setdefault('business_5_0', {
        'human_centered': '',
        'data_driven': '',
        'sustainable': '',
        'automation': '',
        'ethical_ai': '',
    })

    return {
        'mode': 'ai',
        'provider': 'openai',
        'payload': payload,
    }


def chat_response_json(message, history=None):
    """Devuelve estructura JSON empresarial 5.0.

    Si AI_ENABLED=true y hay OPENAI_API_KEY, usa proveedor IA.
    Si falla o no está habilitada, usa motor local.
    """
    history = history or []
    ai_enabled = os.getenv('AI_ENABLED', 'false').lower() in ('1', 'true', 'yes')

    if ai_enabled:
        try:
            return _ask_openai_json(message, history)
        except RuntimeError:
            # fallback seguro sin ocultar errores en la respuesta final
            pass

    return _local_response(message, history)
