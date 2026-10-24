import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  ActivityIndicator,
  Alert,
  TextInput,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { tutorService, tutoriaService } from '../../services/api';

const DIAS = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];
const DURACIONES = [30, 60, 90, 120];
const NIVELES = {
  principiante: 'Principiante',
  intermedio: 'Intermedio',
  avanzado: 'Avanzado',
  experto: 'Experto',
};

const pad = (n) => String(n).padStart(2, '0');
const claveMes = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}`;

function formatearFecha(fecha) {
  const [y, m, d] = fecha.split('-').map(Number);
  const texto = new Date(y, m - 1, d).toLocaleDateString('es-CO', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
  });
  return texto.charAt(0).toUpperCase() + texto.slice(1);
}

function mensajeError(e) {
  const data = e?.response?.data;
  if (!data) return 'No se pudo conectar con el servidor. Revisa tu conexión.';
  if (typeof data === 'string') return data;
  if (data.detail) return String(data.detail);
  const primero = Object.values(data)[0];
  return Array.isArray(primero) ? String(primero[0]) : 'No se pudo registrar la tutoría.';
}

export default function TutorDetailScreen({ navigation, route }) {
  const { tutorId } = route.params || {};
  const hoy = new Date();
  const mesActual = new Date(hoy.getFullYear(), hoy.getMonth(), 1);

  const [tutor, setTutor] = useState(null);
  const [loading, setLoading] = useState(true);
  const [mes, setMes] = useState(mesActual);
  const [duracion, setDuracion] = useState(60);
  const [dispo, setDispo] = useState({ dias: [] });
  const [cargandoDispo, setCargandoDispo] = useState(false);
  const [fechaSel, setFechaSel] = useState(null);
  const [horaSel, setHoraSel] = useState(null);
  const [materiaId, setMateriaId] = useState(null);
  const [lugar, setLugar] = useState('');
  const [guardando, setGuardando] = useState(false);

  useEffect(() => {
    (async () => {
      try {
        const { data } = await tutorService.getById(tutorId);
        setTutor(data);
        if (data.materias?.length) setMateriaId(data.materias[0].id);
      } catch (e) {
        Alert.alert('Error', 'No se pudo cargar el perfil del tutor.');
      } finally {
        setLoading(false);
      }
    })();
  }, [tutorId]);

  const cargarDispo = useCallback(async () => {
    setCargandoDispo(true);
    try {
      const { data } = await tutorService.disponibilidadMensual(tutorId, claveMes(mes), duracion);
      setDispo(data);
    } catch (e) {
      setDispo({ dias: [] });
    } finally {
      setCargandoDispo(false);
    }
  }, [tutorId, mes, duracion]);

  useEffect(() => {
    setFechaSel(null);
    setHoraSel(null);
    cargarDispo();
  }, [cargarDispo]);

  const porFecha = useMemo(() => {
    const mapa = {};
    (dispo.dias || []).forEach((d) => {
      mapa[d.fecha] = d.horarios;
    });
    return mapa;
  }, [dispo]);

  const celdas = useMemo(() => {
    const relleno = (new Date(mes.getFullYear(), mes.getMonth(), 1).getDay() + 6) % 7;
    const total = new Date(mes.getFullYear(), mes.getMonth() + 1, 0).getDate();
    const lista = [];
    for (let i = 0; i < relleno; i++) lista.push({ key: `p${i}`, vacio: true });
    for (let d = 1; d <= total; d++) {
      const fecha = `${claveMes(mes)}-${pad(d)}`;
      lista.push({ key: fecha, d, fecha, libre: !!porFecha[fecha] });
    }
    return lista;
  }, [mes, porFecha]);

  const cambiarMes = (delta) => {
    const nuevo = new Date(mes.getFullYear(), mes.getMonth() + delta, 1);
    if (nuevo < mesActual) return;
    setMes(nuevo);
  };

  const etiquetaMes = mes.toLocaleDateString('es-CO', { month: 'long', year: 'numeric' }).toUpperCase();
  const horarios = fechaSel ? porFecha[fechaSel] || [] : [];

  const agendar = async () => {
    if (!fechaSel || !horaSel) {
      Alert.alert('Selección requerida', 'Elige un día y un horario disponibles.');
      return;
    }
    if (!materiaId) {
      Alert.alert('Selección requerida', 'Este tutor no tiene materias asociadas.');
      return;
    }
    setGuardando(true);
    try {
      await tutoriaService.create({
        tutor: tutor.id,
        materia: materiaId,
        fecha_inicio: `${fechaSel}T${horaSel}:00-05:00`,
        duracion_minutos: duracion,
        lugar: lugar.trim() || 'Por definir con el tutor',
      });
      Alert.alert(
        'Tutoría registrada',
        `${formatearFecha(fechaSel)} a las ${horaSel} con ${tutor.usuario_nombre}.`,
        [{ text: 'Ver mis tutorías', onPress: () => navigation.navigate('Main', { screen: 'Tutorias' }) }]
      );
      setHoraSel(null);
      cargarDispo();
    } catch (e) {
      Alert.alert('No se pudo registrar', mensajeError(e));
      cargarDispo();
    } finally {
      setGuardando(false);
    }
  };

  if (loading) {
    return (
      <View style={[styles.root, styles.center]}>
        <ActivityIndicator size="large" color="#34A853" />
      </View>
    );
  }

  if (!tutor) {
    return (
      <View style={[styles.root, styles.center]}>
        <Text style={styles.bioLarge}>No se encontró el tutor.</Text>
        <TouchableOpacity onPress={() => navigation.goBack()}>
          <Text style={styles.link}>Volver</Text>
        </TouchableOpacity>
      </View>
    );
  }

  const materiaSel = tutor.materias?.find((m) => m.id === materiaId);

  return (
    <View style={styles.root}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <MaterialCommunityIcons name="arrow-left" size={24} color="#34A853" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Perfil del tutor</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView style={styles.scroll} contentContainerStyle={styles.content}>
        <View style={styles.hero}>
          <View style={styles.profileBox}>
            <View style={styles.profileImgPlaceholder}>
              <MaterialCommunityIcons name="account" size={120} color="#DDD" />
            </View>
            <View style={styles.ratingBadgeLarge}>
              <MaterialCommunityIcons name="star" size={20} color="#fff" />
              <Text style={styles.ratingNumLarge}>{Number(tutor.calificacion ?? 0).toFixed(1)}</Text>
            </View>
          </View>

          <Text style={styles.roleKicker}>{(NIVELES[tutor.nivel_experiencia] || 'Tutor').toUpperCase()}</Text>
          <Text style={styles.nameLarge}>{tutor.usuario_nombre}</Text>
          <Text style={styles.especialidad}>{tutor.especialidad}</Text>

          <View style={styles.skillsRow}>
            {(tutor.materias || []).map((m, i) => (
              <View key={m.id} style={i === 0 ? styles.skillPillActive : styles.skillPill}>
                <Text style={i === 0 ? styles.skillTextActive : styles.skillText}>{m.nombre}</Text>
              </View>
            ))}
          </View>

          <View style={styles.statsRowLarge}>
            <View style={styles.statLarge}>
              <Text style={styles.statNumLarge}>{tutor.total_tutorias ?? 0}</Text>
              <Text style={styles.statLblLarge}>TUTORÍAS</Text>
            </View>
            <View style={styles.statLarge}>
              <Text style={styles.statNumLarge}>{tutor.total_resenas ?? 0}</Text>
              <Text style={styles.statLblLarge}>RESEÑAS</Text>
            </View>
            <View style={styles.statLarge}>
              <Text style={styles.statNumLarge}>${Number(tutor.tarifa_por_hora ?? 0).toLocaleString('es-CO')}</Text>
              <Text style={styles.statLblLarge}>POR HORA</Text>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Sobre mí</Text>
            <Text style={styles.bioLarge}>
              {tutor.bio || 'Este tutor aún no ha agregado una descripción.'}
            </Text>
            <View style={styles.badgeSection}>
              <View style={styles.infoBadge}>
                <View style={styles.badgeIconBox}>
                  <MaterialCommunityIcons name="check-decagram" size={20} color="#34A853" />
                </View>
                <View>
                  <Text style={styles.badgeTitle}>Tutor UdeC</Text>
                  <Text style={styles.badgeSub}>{tutor.disponible ? 'Disponible para tutorías' : 'No disponible por ahora'}</Text>
                </View>
              </View>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Disponibilidad mensual</Text>

            <Text style={styles.label}>MATERIA</Text>
            <View style={styles.chipsRow}>
              {(tutor.materias || []).map((m) => (
                <TouchableOpacity
                  key={m.id}
                  style={m.id === materiaId ? styles.timeSlotPillActive : styles.timeSlotPill}
                  onPress={() => setMateriaId(m.id)}
                >
                  <Text style={m.id === materiaId ? styles.timeSlotTextActive : styles.timeSlotText}>{m.nombre}</Text>
                </TouchableOpacity>
              ))}
            </View>

            <Text style={styles.label}>DURACIÓN</Text>
            <View style={styles.chipsRow}>
              {DURACIONES.map((d) => (
                <TouchableOpacity
                  key={d}
                  style={d === duracion ? styles.timeSlotPillActive : styles.timeSlotPill}
                  onPress={() => setDuracion(d)}
                >
                  <Text style={d === duracion ? styles.timeSlotTextActive : styles.timeSlotText}>{d} min</Text>
                </TouchableOpacity>
              ))}
            </View>

            <View style={styles.monthHeader}>
              <TouchableOpacity onPress={() => cambiarMes(-1)} disabled={mes <= mesActual} style={styles.monthBtn}>
                <MaterialCommunityIcons name="chevron-left" size={26} color={mes <= mesActual ? '#DDD' : '#333'} />
              </TouchableOpacity>
              <Text style={styles.monthLabel}>{etiquetaMes}</Text>
              <TouchableOpacity onPress={() => cambiarMes(1)} style={styles.monthBtn}>
                <MaterialCommunityIcons name="chevron-right" size={26} color="#333" />
              </TouchableOpacity>
            </View>

            <View style={styles.weekRow}>
              {DIAS.map((d) => (
                <Text key={d} style={styles.calDayText}>{d}</Text>
              ))}
            </View>
            {cargandoDispo ? (
              <ActivityIndicator style={{ marginVertical: 24 }} color="#34A853" />
            ) : (
              <View style={styles.calendarGrid}>
                {celdas.map((c) =>
                  c.vacio ? (
                    <View key={c.key} style={styles.calCell} />
                  ) : (
                    <TouchableOpacity
                      key={c.key}
                      style={styles.calCell}
                      disabled={!c.libre}
                      onPress={() => {
                        setFechaSel(c.fecha);
                        setHoraSel(null);
                      }}
                    >
                      <View
                        style={[
                          styles.calDateBox,
                          c.libre && styles.calDateBoxHighlight,
                          c.fecha === fechaSel && styles.calDateBoxActive,
                        ]}
                      >
                        <Text
                          style={[
                            styles.calDateText,
                            !c.libre && styles.calDateTextMuted,
                            c.fecha === fechaSel && styles.calDateTextActive,
                          ]}
                        >
                          {c.d}
                        </Text>
                      </View>
                    </TouchableOpacity>
                  )
                )}
              </View>
            )}
            {!cargandoDispo && (dispo.dias || []).length === 0 && (
              <Text style={styles.emptyText}>No hay horarios libres este mes. Prueba el mes siguiente.</Text>
            )}

            {fechaSel && (
              <>
                <Text style={styles.selectedDateText}>Seleccionado: {formatearFecha(fechaSel)}</Text>
                <View style={styles.timeSlotsGrid}>
                  {horarios.map((h) => (
                    <TouchableOpacity
                      key={h}
                      style={h === horaSel ? styles.timeSlotPillActive : styles.timeSlotPill}
                      onPress={() => setHoraSel(h)}
                    >
                      <Text style={h === horaSel ? styles.timeSlotTextActive : styles.timeSlotText}>{h}</Text>
                    </TouchableOpacity>
                  ))}
                </View>
              </>
            )}

            <Text style={styles.label}>LUGAR O ENLACE (opcional)</Text>
            <TextInput
              style={styles.input}
              placeholder="Salón, biblioteca, enlace de Meet..."
              placeholderTextColor="#999"
              value={lugar}
              onChangeText={setLugar}
            />

            <View style={styles.infoBoxMuted}>
              <MaterialCommunityIcons name="information" size={18} color="#B8860B" />
              <Text style={styles.infoBoxText}>
                Los días en verde tienen horarios libres. La tutoría queda registrada como pendiente hasta que el tutor la confirme.
              </Text>
            </View>
          </View>

          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Reseñas</Text>
            {(tutor.resenas || []).length === 0 ? (
              <Text style={styles.bioLarge}>Aún no hay reseñas para este tutor.</Text>
            ) : (
              tutor.resenas.map((r, i) => (
                <View key={i} style={styles.resena}>
                  <View style={styles.resenaTop}>
                    <Text style={styles.badgeTitle}>{r.estudiante}</Text>
                    <View style={styles.resenaStars}>
                      <MaterialCommunityIcons name="star" size={14} color="#FBC02D" />
                      <Text style={styles.badgeTitle}>{Number(r.calificacion).toFixed(1)}</Text>
                    </View>
                  </View>
                  {!!r.comentario && <Text style={styles.badgeSub}>{r.comentario}</Text>}
                </View>
              ))
            )}
          </View>
        </View>
      </ScrollView>

      <TouchableOpacity
        style={[styles.bookBtnLarge, (!horaSel || guardando) && { opacity: 0.6 }]}
        activeOpacity={0.9}
        disabled={guardando}
        onPress={agendar}
      >
        <View style={styles.bookBtnTextContainer}>
          <Text style={styles.bookBtnKicker}>
            {horaSel ? `${formatearFecha(fechaSel)} · ${horaSel} · ${duracion} min` : 'ELIGE UN DÍA Y UN HORARIO'}
          </Text>
          <Text style={styles.bookBtnMainText}>
            {guardando ? 'Registrando...' : `Agendar${materiaSel ? ` ${materiaSel.nombre}` : ''}`}
          </Text>
        </View>
        <View style={styles.bookBtnIconBox}>
          <MaterialCommunityIcons name="calendar-plus" size={24} color="#fff" />
        </View>
      </TouchableOpacity>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#fff' },
  center: { justifyContent: 'center', alignItems: 'center' },
  link: { color: '#34A853', fontWeight: 'bold', marginTop: 12 },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 50,
    paddingBottom: 10,
  },
  backBtn: { width: 40, height: 40, justifyContent: 'center' },
  headerTitle: { fontSize: 18, fontWeight: 'bold', color: '#34A853' },
  scroll: { flex: 1 },
  content: { paddingBottom: 140 },
  hero: { padding: 20 },
  profileBox: { width: '100%', height: 240, borderRadius: 32, backgroundColor: '#F0F0F0', marginBottom: 24, position: 'relative' },
  profileImgPlaceholder: { flex: 1, borderRadius: 32, justifyContent: 'center', alignItems: 'center' },
  ratingBadgeLarge: {
    position: 'absolute',
    right: 20,
    top: 20,
    backgroundColor: '#FFB300',
    paddingHorizontal: 12,
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
    gap: 2,
    elevation: 4,
  },
  ratingNumLarge: { fontSize: 14, fontWeight: 'bold', color: '#fff' },
  roleKicker: { fontSize: 10, fontWeight: 'bold', color: '#34A853', letterSpacing: 1 },
  nameLarge: { fontSize: 30, fontWeight: 'bold', color: '#333', marginTop: 8 },
  especialidad: { fontSize: 15, color: '#666', marginTop: 4 },
  skillsRow: { flexDirection: 'row', gap: 8, marginTop: 16, flexWrap: 'wrap' },
  skillPill: { backgroundColor: '#F0F0F0', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  skillPillActive: { backgroundColor: '#A5D6A7', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  skillText: { fontSize: 12, fontWeight: '600', color: '#666' },
  skillTextActive: { fontSize: 12, fontWeight: '600', color: '#006D32' },
  statsRowLarge: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 24, paddingVertical: 8 },
  statLarge: { alignItems: 'flex-start' },
  statNumLarge: { fontSize: 20, fontWeight: 'bold', color: '#333' },
  statLblLarge: { fontSize: 9, color: '#999', marginTop: 4, fontWeight: 'bold' },
  section: { marginTop: 28 },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#333', marginBottom: 12 },
  bioLarge: { fontSize: 14, color: '#666', lineHeight: 22, marginBottom: 16 },
  badgeSection: { gap: 12, marginBottom: 8 },
  infoBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: '#F9F9F9', padding: 12, borderRadius: 16, gap: 12 },
  badgeIconBox: { width: 36, height: 36, borderRadius: 18, backgroundColor: '#E8F5E9', justifyContent: 'center', alignItems: 'center' },
  badgeTitle: { fontSize: 14, fontWeight: 'bold', color: '#333' },
  badgeSub: { fontSize: 12, color: '#777', marginTop: 2 },
  label: { fontSize: 11, fontWeight: 'bold', color: '#666', marginBottom: 8, marginTop: 8, letterSpacing: 1 },
  chipsRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 8 },
  monthHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginTop: 16, marginBottom: 12 },
  monthBtn: { width: 40, height: 40, justifyContent: 'center', alignItems: 'center' },
  monthLabel: { fontSize: 13, fontWeight: 'bold', color: '#333', letterSpacing: 1 },
  weekRow: { flexDirection: 'row', marginBottom: 4 },
  calendarGrid: { flexDirection: 'row', flexWrap: 'wrap', marginBottom: 16 },
  calCell: { width: '14.2857%', alignItems: 'center', marginBottom: 6 },
  calDayText: { width: '14.2857%', textAlign: 'center', fontSize: 12, color: '#999', fontWeight: 'bold' },
  calDateBox: { width: 38, height: 38, justifyContent: 'center', alignItems: 'center', borderRadius: 12 },
  calDateBoxActive: { backgroundColor: '#34A853' },
  calDateBoxHighlight: { backgroundColor: '#E8F5E9' },
  calDateText: { fontSize: 14, color: '#333', fontWeight: '600' },
  calDateTextActive: { color: '#fff' },
  calDateTextMuted: { color: '#CCC', fontWeight: '400' },
  emptyText: { fontSize: 13, color: '#B8860B', marginBottom: 12, textAlign: 'center' },
  selectedDateText: { fontSize: 14, fontWeight: 'bold', color: '#333', marginBottom: 12 },
  timeSlotsGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 16 },
  timeSlotPill: { backgroundColor: '#F0F0F0', paddingHorizontal: 14, paddingVertical: 10, borderRadius: 16 },
  timeSlotPillActive: { backgroundColor: '#006D32', paddingHorizontal: 14, paddingVertical: 10, borderRadius: 16 },
  timeSlotText: { fontSize: 14, fontWeight: '600', color: '#666' },
  timeSlotTextActive: { fontSize: 14, fontWeight: '600', color: '#fff' },
  input: { backgroundColor: '#F0F0F0', borderRadius: 16, paddingHorizontal: 16, height: 48, fontSize: 14, color: '#333', marginBottom: 16 },
  infoBoxMuted: { flexDirection: 'row', alignItems: 'center', gap: 8, backgroundColor: '#FFF9E6', padding: 12, borderRadius: 12 },
  infoBoxText: { fontSize: 12, color: '#B8860B', flex: 1 },
  resena: { backgroundColor: '#F9F9F9', padding: 12, borderRadius: 16, marginBottom: 8 },
  resenaTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  resenaStars: { flexDirection: 'row', alignItems: 'center', gap: 3 },
  bookBtnLarge: {
    position: 'absolute',
    bottom: 30,
    left: 20,
    right: 20,
    backgroundColor: '#006D32',
    height: 70,
    borderRadius: 35,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    elevation: 10,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 10,
    shadowOffset: { width: 0, height: 4 },
  },
  bookBtnTextContainer: { flex: 1 },
  bookBtnKicker: { color: 'rgba(255,255,255,0.7)', fontSize: 10, fontWeight: 'bold' },
  bookBtnMainText: { color: '#fff', fontSize: 17, fontWeight: 'bold' },
  bookBtnIconBox: { width: 44, height: 44, borderRadius: 22, backgroundColor: 'rgba(255,255,255,0.2)', justifyContent: 'center', alignItems: 'center' },
});
