<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div>
        <p class="eyebrow">ANÁLISIS EXPLORATORIO</p>
        <h1>Dashboard académico</h1>
        <p class="muted">
          Indicadores de la plataforma. Se actualiza automáticamente cada 30
          segundos.
        </p>
      </div>
      <button type="button" :disabled="loading" @click="loadSummary">
        {{ loading ? 'Actualizando…' : 'Actualizar ahora' }}
      </button>
    </header>

    <p v-if="error" class="error" role="alert">{{ error }}</p>
    <p v-else-if="loading && !summary" class="muted">Cargando indicadores…</p>

    <template v-if="summary">
      <section class="metrics" aria-label="Indicadores principales">
        <article class="metric">
          <span>Usuarios</span>
          <strong>{{ summary.indicadores.usuarios }}</strong>
        </article>
        <article class="metric">
          <span>Tutores</span>
          <strong>{{ summary.indicadores.tutores }}</strong>
        </article>
        <article class="metric">
          <span>Materias</span>
          <strong>{{ summary.indicadores.materias }}</strong>
        </article>
        <article class="metric">
          <span>Tutorías</span>
          <strong>{{ summary.indicadores.tutorias }}</strong>
        </article>
        <article class="metric">
          <span>Calificación promedio</span>
          <strong>{{ summary.indicadores.calificacion_promedio.toFixed(2) }}</strong>
        </article>
      </section>

      <section class="charts">
        <article class="panel">
          <h2>Tutorías por mes</h2>
          <div
            class="bar-chart"
            role="img"
            aria-label="Cantidad de tutorías por mes durante los últimos seis meses"
          >
            <div
              v-for="item in summary.tutorias_por_mes"
              :key="item.mes"
              class="bar-column"
            >
              <span class="bar-value">{{ item.total }}</span>
              <div
                class="bar"
                :style="{ height: barHeight(item.total, monthlyMaximum) }"
              ></div>
              <span class="bar-label">{{ monthLabel(item.mes) }}</span>
            </div>
          </div>
        </article>

        <article class="panel">
          <h2>Estado de las tutorías</h2>
          <ul class="distribution">
            <li
              v-for="item in summary.tutorias_por_estado"
              :key="item.estado"
            >
              <div class="distribution-label">
                <span>{{ item.etiqueta }}</span>
                <strong>{{ item.total }}</strong>
              </div>
              <div class="track">
                <div
                  class="fill"
                  :style="{ width: percentage(item.total, summary.indicadores.tutorias) }"
                ></div>
              </div>
            </li>
          </ul>
        </article>

        <article class="panel panel-wide">
          <h2>Materias con más tutorías</h2>
          <p v-if="summary.tutorias_por_materia.length === 0" class="muted">
            Aún no hay materias registradas.
          </p>
          <ol v-else class="subjects">
            <li
              v-for="item in summary.tutorias_por_materia"
              :key="item.nombre"
            >
              <span>{{ item.nombre }}</span>
              <strong>{{ item.total }}</strong>
            </li>
          </ol>
        </article>
      </section>

      <p class="updated">
        Última actualización:
        {{ new Date(summary.actualizado_en).toLocaleString('es-CO') }}
      </p>
    </template>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { dashboardApi } from '@/services/api';

const summary = ref(null);
const loading = ref(false);
const error = ref('');
let refreshTimer;

const monthlyMaximum = computed(() =>
  Math.max(1, ...(summary.value?.tutorias_por_mes ?? []).map((item) => item.total))
);

function barHeight(value, maximum) {
  return `${Math.max(4, (value / maximum) * 150)}px`;
}

function percentage(value, total) {
  return `${total ? (value / total) * 100 : 0}%`;
}

function monthLabel(month) {
  const [year, number] = month.split('-').map(Number);
  return new Date(year, number - 1, 1).toLocaleDateString('es-CO', {
    month: 'short',
  });
}

async function loadSummary() {
  loading.value = true;
  error.value = '';
  try {
    const { data } = await dashboardApi.resumen();
    summary.value = data;
  } catch (requestError) {
    error.value =
      requestError.response?.data?.detail ||
      'No se pudieron cargar los indicadores del dashboard.';
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadSummary();
  refreshTimer = window.setInterval(loadSummary, 30000);
});

onUnmounted(() => {
  window.clearInterval(refreshTimer);
});
</script>

<style scoped>
.dashboard {
  max-width: 1180px;
  margin: 0 auto;
  padding: 2rem 1rem 3rem;
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.eyebrow {
  margin: 0 0 0.4rem;
  color: #2e7d32;
  font-size: 0.75rem;
  font-weight: 800;
  letter-spacing: 0.12em;
}

h1,
h2 {
  margin: 0;
}

h1 {
  font-size: clamp(1.6rem, 4vw, 2.2rem);
}

h2 {
  margin-bottom: 1.25rem;
  font-size: 1.1rem;
}

.muted {
  color: #666;
}

.dashboard-header .muted {
  margin: 0.5rem 0 0;
}

button {
  flex: 0 0 auto;
  border: 0;
  border-radius: 8px;
  padding: 0.7rem 1rem;
  background: #34a853;
  color: #fff;
  font-weight: 700;
  cursor: pointer;
}

button:disabled {
  cursor: wait;
  opacity: 0.65;
}

.error {
  color: #b42318;
}

.metrics {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.metric,
.panel {
  border: 1px solid #e4e8ed;
  border-radius: 12px;
  background: #fff;
  box-shadow: 0 4px 16px rgba(22, 36, 50, 0.05);
}

.metric {
  display: grid;
  gap: 0.6rem;
  padding: 1rem 1.1rem;
}

.metric span,
.bar-label {
  color: #667085;
  font-size: 0.88rem;
}

.metric strong {
  color: #263238;
  font-size: 1.8rem;
}

.charts {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.panel {
  padding: 1.25rem;
}

.panel-wide {
  grid-column: 1 / -1;
}

.bar-chart {
  display: flex;
  align-items: flex-end;
  justify-content: space-around;
  gap: 0.5rem;
  min-height: 205px;
  padding-top: 1.25rem;
}

.bar-column {
  display: flex;
  flex: 1;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 0.45rem;
  height: 205px;
}

.bar-value {
  color: #475467;
  font-size: 0.8rem;
}

.bar {
  width: min(48px, 70%);
  min-height: 4px;
  border-radius: 6px 6px 0 0;
  background: linear-gradient(180deg, #59c36a, #23823a);
}

.bar-label {
  text-transform: capitalize;
}

.distribution,
.subjects {
  margin: 0;
  padding: 0;
  list-style: none;
}

.distribution {
  display: grid;
  gap: 1rem;
}

.distribution-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.35rem;
  color: #475467;
  font-size: 0.9rem;
}

.track {
  height: 8px;
  overflow: hidden;
  border-radius: 999px;
  background: #edf0f2;
}

.fill {
  height: 100%;
  border-radius: inherit;
  background: #34a853;
}

.subjects li {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eef0f2;
}

.subjects li:last-child {
  border-bottom: 0;
}

.updated {
  margin-top: 1rem;
  color: #667085;
  font-size: 0.8rem;
  text-align: right;
}

@media (max-width: 640px) {
  .dashboard-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .charts {
    grid-template-columns: 1fr;
  }
}
</style>
