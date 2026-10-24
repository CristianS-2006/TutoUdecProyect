"""Análisis exploratorio de datos (EDA) de TutoUdec.

Lee los datos públicos de la API (por defecto la de Azure), calcula estadísticas
y genera gráficas y un informe en Markdown dentro de analytics/output.

Uso:
    python analytics/eda_tutoudec.py [URL_API]
"""
import json
import sys
import urllib.request
from pathlib import Path

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

API = (sys.argv[1] if len(sys.argv) > 1 else 'http://4.206.201.129/api').rstrip('/')
OUT = Path(__file__).parent / 'output'
OUT.mkdir(exist_ok=True)
GREEN = '#007F3F'
NIVEL_ORDEN = ['principiante', 'intermedio', 'avanzado', 'experto']


def fetch(resource):
    url = f'{API}/{resource}/'
    items = []
    while url:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = json.loads(resp.read().decode('utf-8'))
        if not isinstance(data, dict):
            return data
        items += data['results']
        url = data.get('next')
    return items


def save(fig, name):
    fig.tight_layout()
    fig.savefig(OUT / name, dpi=130)
    plt.close(fig)


def table_md(df):
    cols = [df.index.name or ''] + [str(c) for c in df.columns]
    rows = ['| ' + ' | '.join(cols) + ' |', '|' + '---|' * len(cols)]
    for idx, r in df.iterrows():
        rows.append('| ' + ' | '.join([str(idx)] + [str(v) for v in r.tolist()]) + ' |')
    return '\n'.join(rows)


tutores = pd.DataFrame(fetch('tutores'))
materias = pd.DataFrame(fetch('materias'))
disp = pd.DataFrame(fetch('disponibilidades'))

tutores['tarifa_por_hora'] = pd.to_numeric(tutores['tarifa_por_hora'])
tutores['nivel_experiencia'] = pd.Categorical(
    tutores['nivel_experiencia'], categories=NIVEL_ORDEN, ordered=True
)
disp['horas'] = (
    pd.to_datetime(disp['hora_fin'], format='%H:%M:%S')
    - pd.to_datetime(disp['hora_inicio'], format='%H:%M:%S')
).dt.total_seconds() / 3600

tarifa_nivel = tutores.groupby('nivel_experiencia', observed=True)['tarifa_por_hora'].agg(['count', 'mean', 'min', 'max'])
calif_nivel = tutores.groupby('nivel_experiencia', observed=True)['calificacion'].mean().to_frame('calificacion')
esp = tutores['especialidad'].value_counts()
dias = disp.groupby(['dia_semana', 'dia_semana_display']).size().reset_index(name='franjas').sort_values('dia_semana')
horas_tutor = disp.groupby('tutor_nombre')['horas'].sum().sort_values(ascending=False)
mat_top = materias.sort_values('total_tutorias', ascending=False).head(10)
corr = tutores['tarifa_por_hora'].corr(tutores['calificacion'])

fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(tutores['tarifa_por_hora'], bins=8, color=GREEN, edgecolor='white')
ax.set(title='Distribución de tarifas por hora', xlabel='COP por hora', ylabel='Tutores')
save(fig, '01_tarifas.png')

fig, ax = plt.subplots(figsize=(7, 4))
tarifa_nivel['mean'].plot.bar(ax=ax, color=GREEN, rot=0)
ax.set(title='Tarifa promedio por nivel de experiencia', xlabel='', ylabel='COP por hora')
save(fig, '02_tarifa_nivel.png')

fig, ax = plt.subplots(figsize=(7, 4))
esp.sort_values().plot.barh(ax=ax, color=GREEN)
ax.set(title='Tutores por especialidad', xlabel='Tutores', ylabel='')
save(fig, '03_especialidades.png')

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(dias['dia_semana_display'], dias['franjas'], color=GREEN)
ax.set(title='Franjas de disponibilidad por día', ylabel='Franjas')
save(fig, '04_disponibilidad_dia.png')

fig, ax = plt.subplots(figsize=(7, 4))
ax.scatter(tutores['tarifa_por_hora'], tutores['calificacion'], color=GREEN)
ax.set(title='Tarifa vs calificación' + (f' (correlación {corr:.2f})' if pd.notna(corr) else ''), xlabel='COP por hora', ylabel='Calificación')
save(fig, '05_tarifa_vs_calificacion.png')

fig, ax = plt.subplots(figsize=(7, 4))
mat_top.set_index('nombre')['total_tutorias'].sort_values().plot.barh(ax=ax, color=GREEN)
ax.set(title='Materias con más tutorías', xlabel='Tutorías', ylabel='')
save(fig, '06_materias_top.png')

dias_ord = dias.sort_values('franjas')
lines = [
    '# Análisis exploratorio de datos — TutoUdec',
    '',
    f'Fuente: `{API}` · {len(tutores)} tutores, {len(materias)} materias, {len(disp)} franjas de disponibilidad.',
    '',
    '## Hallazgos',
    f'- Tarifa promedio: **${tutores["tarifa_por_hora"].mean():,.0f} COP/h** (mín ${tutores["tarifa_por_hora"].min():,.0f}, máx ${tutores["tarifa_por_hora"].max():,.0f}).',
    f'- Calificación promedio de los tutores: **{tutores["calificacion"].mean():.2f}**.',
    (
        f'- Correlación tarifa–calificación: **{corr:.2f}**.'
        if pd.notna(corr)
        else '- Correlación tarifa–calificación: no calculable (todas las calificaciones son iguales; aún no hay reseñas reales).'
    ),
    f'- Especialidad con más tutores: **{esp.index[0]}** ({esp.iloc[0]}).',
    f'- Día con más disponibilidad: **{dias_ord.iloc[-1]["dia_semana_display"]}**; con menos: **{dias_ord.iloc[0]["dia_semana_display"]}**.',
    f'- Tutor con más horas ofrecidas por semana: **{horas_tutor.index[0]}** ({horas_tutor.iloc[0]:.0f} h).',
    f'- Materias sin tutorías registradas: **{int((materias["total_tutorias"] == 0).sum())}** de {len(materias)}.',
    '',
    '## Tarifa por nivel',
    table_md(tarifa_nivel.round(0)),
    '',
    '## Calificación promedio por nivel',
    table_md(calif_nivel.round(2)),
    '',
    '## Gráficas',
    *[f'![{p.stem}]({p.name})' for p in sorted(OUT.glob('*.png'))],
    '',
    '_Nota: los datos actuales son de prueba (seed_data); las conclusiones deben releerse con datos reales._',
]
(OUT / 'informe_eda.md').write_text('\n'.join(lines), encoding='utf-8')
print('\n'.join(lines[:14]))
