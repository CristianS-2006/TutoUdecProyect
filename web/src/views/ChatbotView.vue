<template>
  <div class="page">
    <h1>Asistente TutoUdec</h1>
    <p class="muted">Pregúntame sobre las tutorías y la Universidad de Cundinamarca.</p>

    <div ref="box" class="chat">
      <div v-for="(m, i) in messages" :key="i" :class="['msg', m.sender]">
        <span class="bubble">{{ m.text }}</span>
      </div>
      <p v-if="loading" class="muted">Escribiendo…</p>
    </div>

    <div class="chips">
      <button v-for="s in suggestions" :key="s" type="button" @click="send(s)">{{ s }}</button>
    </div>

    <form class="row" @submit.prevent="send(input)">
      <input v-model="input" placeholder="Escribe tu pregunta…" maxlength="500" />
      <button type="submit" :disabled="loading || !input.trim()">Enviar</button>
    </form>
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref } from 'vue';
import { api } from '@/services/api';

const messages = ref([
  {
    sender: 'bot',
    text: '¡Hola! Soy el asistente de TutoUdec. Puedo ayudarte con tutorías, materias, tu cuenta y la Universidad de Cundinamarca.',
  },
]);
const suggestions = ref([]);
const input = ref('');
const loading = ref(false);
const box = ref(null);

onMounted(async () => {
  try {
    const { data } = await api.get('/chatbot/quick_questions/');
    suggestions.value = data.quick_questions;
  } catch {
    suggestions.value = [];
  }
});

async function send(text) {
  const message = text.trim();
  if (!message || loading.value) return;
  const history = messages.value.filter((m) => m.intent).slice(-6).map((m) => ({ intent: m.intent }));
  messages.value.push({ sender: 'user', text: message });
  input.value = '';
  loading.value = true;
  try {
    const { data } = await api.post('/chatbot/chat/', { message, history });
    messages.value.push({ sender: 'bot', text: data.bot_response, intent: data.intent });
    if (data.suggestions?.length) suggestions.value = data.suggestions;
  } catch {
    messages.value.push({ sender: 'bot', text: 'No pude conectarme con el servidor. Intenta de nuevo.' });
  } finally {
    loading.value = false;
    await nextTick();
    if (box.value) box.value.scrollTop = box.value.scrollHeight;
  }
}
</script>

<style scoped>
.page { max-width: 760px; margin: 0 auto; padding: 1.5rem 1rem 3rem; }
.muted { color: #666; }
.chat { height: 380px; overflow-y: auto; background: #fff; border-radius: 10px; padding: 1rem; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06); }
.msg { display: flex; margin-bottom: 0.6rem; }
.msg.user { justify-content: flex-end; }
.bubble { white-space: pre-line; max-width: 80%; padding: 0.6rem 0.9rem; border-radius: 14px; background: #f1f3f4; }
.msg.user .bubble { background: #34a853; color: #fff; }
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.8rem 0; }
.chips button { border: 1px solid #34a853; background: #e8f5e9; color: #2e7d32; border-radius: 999px; padding: 0.3rem 0.8rem; cursor: pointer; }
.row { display: flex; gap: 0.5rem; }
.row input { flex: 1; padding: 0.6rem; border: 1px solid #ccc; border-radius: 8px; }
.row button { padding: 0.6rem 1.2rem; border: 0; border-radius: 8px; background: #34a853; color: #fff; cursor: pointer; }
.row button:disabled { opacity: 0.5; cursor: default; }
</style>
