import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
  Alert,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AppHeader from '../../components/AppHeader';
import { tutoriaService } from '../../services/api';
import { C } from '../../theme/colors';

const AVATAR =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDVcwn6s4nV1CHSNpmpipBJK0bu9UNLelccnDqAHqmn7QUlTePVc_DbrcM_JX2z9MgKGXvfnI2AzQG0IEvmbYFSUI6AfERimpAo9FkFyHLLAXKw0x7OBblhNYt4i2vJhIq_rZMEi3IPzG0MRpxEZBH7m-prN9iibsqFPtjwwEcTMUY_KfpEt5xgXYOU-KXKYE_q_W7YI7YUjPLUgCvD5qa5vaoPbh0MN5JNhYetwk78LyAkMZ9GzqGpSWEPAEnTSyP_w4l1KUi3KGw';

function listPayload(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}

const WEEK = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];

export default function TutoriasScreen({ navigation }) {
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [selected, setSelected] = useState(() => new Date());

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const { data } = await tutoriaService.getMisTutorias({ page_size: 60 });
      setItems(listPayload(data));
    } catch (e) {
      console.warn('Tutorias', e.message);
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    load();
  }, [load]);

  const onRefresh = async () => {
    setRefreshing(true);
    await load();
    setRefreshing(false);
  };

  const daysWithEvents = useMemo(() => {
    const set = new Set();
    items.forEach((t) => {
      if (!t.fecha_inicio) return;
      const d = new Date(t.fecha_inicio);
      set.add(`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`);
    });
    return set;
  }, [items]);

  const calendarDays = useMemo(() => {
    const y = selected.getFullYear();
    const m = selected.getMonth();
    const first = new Date(y, m, 1);
    const startPad = (first.getDay() + 6) % 7;
    const daysInMonth = new Date(y, m + 1, 0).getDate();
    const cells = [];
    for (let i = 0; i < startPad; i++) cells.push({ type: 'pad', key: `p-${i}` });
    for (let d = 1; d <= daysInMonth; d++) {
      cells.push({ type: 'day', d, key: `d-${d}` });
    }
    return cells;
  }, [selected]);

  const selectedKey = `${selected.getFullYear()}-${selected.getMonth()}-${selected.getDate()}`;
  const agenda = items.filter((t) => {
    if (!t.fecha_inicio) return false;
    const d = new Date(t.fecha_inicio);
    return (
      d.getFullYear() === selected.getFullYear() &&
      d.getMonth() === selected.getMonth() &&
      d.getDate() === selected.getDate()
    );
  });

  const monthLabel = selected.toLocaleDateString('es-CO', { month: 'long', year: 'numeric' });

  if (loading) {
    return (
      <View style={styles.root}>
        <AppHeader
          variant="home"
          avatarUri={AVATAR}
          onPressAvatar={() => navigation.navigate('Profile')}
          onPressBell={() => {}}
        />
        <View style={styles.center}>
          <ActivityIndicator size="large" color={C.instGreen} />
        </View>
      </View>
    );
  }

  return (
    <View style={styles.root}>
      <AppHeader
        variant="home"
        avatarUri={AVATAR}
        onPressAvatar={() => navigation.navigate('Profile')}
        onPressBell={() => {}}
      />
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
      <Text style={styles.kicker}>HORARIO ACADÉMICO</Text>
      <Text style={styles.monthTitle}>{monthLabel}</Text>

      <View style={styles.calCard}>
        <View style={styles.weekRow}>
          {WEEK.map((w) => (
            <Text key={w} style={styles.weekCell}>
              {w}
            </Text>
          ))}
        </View>
        <View style={styles.grid}>
          {calendarDays.map((cell) => {
            if (cell.type === 'pad') {
              return <View key={cell.key} style={styles.cell} />;
            }
            const key = `${selected.getFullYear()}-${selected.getMonth()}-${cell.d}`;
            const has = daysWithEvents.has(key);
            const isSel = key === selectedKey;
            return (
              <TouchableOpacity
                key={cell.key}
                style={[styles.cell, isSel && styles.cellSel]}
                onPress={() => setSelected(new Date(selected.getFullYear(), selected.getMonth(), cell.d))}
              >
                <Text style={[styles.cellText, isSel && styles.cellTextSel]}>{cell.d}</Text>
                {has && !isSel ? <View style={styles.dot} /> : null}
              </TouchableOpacity>
            );
          })}
        </View>
      </View>

      <View style={styles.statsBanner}>
        <View style={styles.statsTextContainer}>
          <Text style={styles.statsLbl}>Programadas este mes</Text>
          <Text style={styles.statsNum}>{items.length} Sesiones</Text>
        </View>
        <View style={styles.statsIcon}>
          <MaterialCommunityIcons name="calendar-check" size={24} color="#fff" />
        </View>
      </View>

      <View style={styles.summaryCard}>
        <View style={styles.summaryItem}>
          <Text style={styles.summaryNum}>{items.filter(i => i.estado === 'completada').length}</Text>
          <Text style={styles.summaryLbl}>Completadas</Text>
        </View>
        <View style={styles.summaryDivider} />
        <View style={styles.summaryItem}>
          <Text style={styles.summaryNum}>{items.filter(i => i.estado === 'pendiente').length}</Text>
          <Text style={styles.summaryLbl}>Pendientes</Text>
        </View>
        <View style={styles.summaryDivider} />
        <View style={styles.summaryItem}>
          <Text style={styles.summaryNum}>{items.filter(i => i.estado === 'cancelada').length}</Text>
          <Text style={styles.summaryLbl}>Canceladas</Text>
        </View>
      </View>

      <View style={styles.agendaHead}>
        <View>
          <Text style={styles.kickerSmall}>AGENDA PRÓXIMA</Text>
          <Text style={styles.agendaTitle}>
            {selected.toLocaleDateString('es-CO', { weekday: 'long', day: 'numeric', month: 'short' })}
          </Text>
        </View>
        <TouchableOpacity style={styles.listBtn} onPress={() => navigation.navigate('Tutores')}>
          <Text style={styles.listBtnText}>Ver Lista</Text>
          <MaterialCommunityIcons name="format-list-bulleted" size={18} color="#333" />
        </TouchableOpacity>
      </View>

      {agenda.length === 0 ? (
        <View style={styles.noMoreBox}>
          <Text style={styles.noMoreText}>No hay sesiones para este día.</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Tutores')}>
            <Text style={styles.browseLink}>Explorar tutores disponibles →</Text>
          </TouchableOpacity>
        </View>
      ) : (
        agenda.map((item) => {
          const startTime = item.fecha_inicio ? new Date(item.fecha_inicio) : null;
          const timeStr = startTime ? startTime.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', hour12: false }) : '--:--';
          const isOnline = item.lugar?.toLowerCase().includes('google') || item.lugar?.toLowerCase().includes('online');
          
          return (
            <View key={item.id} style={styles.agendaCard}>
              <View style={styles.timeBoxLarge}>
                <Text style={styles.timeTxtLarge}>{timeStr}</Text>
                <Text style={styles.durTxtSmall}>{item.duracion_minutos || 60}MIN</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.agendaNameLarge}>{item.materia_nombre || 'Tutoría'}</Text>
                <View style={styles.locationRow}>
                  <MaterialCommunityIcons 
                    name={isOnline ? "video-outline" : "map-marker-outline"} 
                    size={14} 
                    color="#34A853" 
                  />
                  <Text style={styles.agendaMetaSmall}>{item.lugar || 'Campus UdeC'}</Text>
                  {isOnline && <View style={styles.onlineBadge}><Text style={styles.onlineBadgeText}>EN LÍNEA</Text></View>}
                </View>
              </View>
              <View style={{ alignItems: 'flex-end', gap: 8 }}>
                <View style={styles.tutorRowSmall}>
                  <View style={[styles.avatarTiny, { backgroundColor: '#34A853' }]} />
                  <View style={styles.tutorPillSmall}>
                    <Text style={styles.tutorPillText}>{item.tutor_nombre || 'Tutor'}</Text>
                  </View>
                </View>
                <TouchableOpacity 
                  style={[styles.detailsBtn, item.estado === 'pendiente' && { backgroundColor: '#006D32' }]}
                  onPress={() => {
                    if (item.estado === 'pendiente') {
                      Alert.alert('Unirse a Sesión', 'Redirigiendo a la sala virtual...');
                    } else {
                      // Show details
                    }
                  }}
                >
                  <Text style={styles.detailsBtnText}>
                    {item.estado === 'pendiente' ? 'UNIRSE' : 'DETALLES'}
                  </Text>
                </TouchableOpacity>
              </View>
            </View>
          );
        })
      )}

      {agenda.length > 0 && (
        <View style={styles.noMoreBox}>
          <Text style={styles.noMoreText}>No hay más sesiones para hoy.</Text>
          <TouchableOpacity onPress={() => navigation.navigate('Tutores')}>
            <Text style={styles.browseLink}>Explorar tutores disponibles →</Text>
          </TouchableOpacity>
        </View>
      )}

      <TouchableOpacity style={styles.fabYellow} onPress={() => navigation.navigate('Add')}>
        <MaterialCommunityIcons name="plus" size={28} color="#333" />
      </TouchableOpacity>
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#fff' },
  scroll: { flex: 1 },
  content: { paddingBottom: 100, paddingHorizontal: 20 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  kicker: { fontSize: 12, fontWeight: 'bold', color: '#34A853', letterSpacing: 1 },
  monthTitle: { fontSize: 28, fontWeight: 'bold', color: '#333', marginBottom: 16, marginTop: 4 },
  calCard: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 16,
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  weekRow: { flexDirection: 'row', marginBottom: 8 },
  weekCell: { flex: 1, textAlign: 'center', fontSize: 12, color: '#999', fontWeight: '600' },
  grid: { flexDirection: 'row', flexWrap: 'wrap' },
  cell: {
    width: '14.28%',
    height: 40,
    justifyContent: 'center',
    alignItems: 'center',
    borderRadius: 20,
  },
  cellSel: { backgroundColor: '#34A853' },
  cellText: { fontSize: 14, color: '#333', fontWeight: '500' },
  cellTextSel: { color: '#fff', fontWeight: 'bold' },
  dot: {
    position: 'absolute',
    bottom: 4,
    width: 4,
    height: 4,
    borderRadius: 2,
    backgroundColor: '#34A853',
  },
  statsBanner: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#E8F5E9',
    borderRadius: 20,
    padding: 20,
    marginBottom: 16,
  },
  statsTextContainer: { flex: 1 },
  statsLbl: { fontSize: 12, color: '#34A853', fontWeight: '600' },
  statsNum: { fontSize: 20, fontWeight: 'bold', color: '#333', marginTop: 4 },
  statsIcon: {
    width: 48,
    height: 48,
    borderRadius: 16,
    backgroundColor: '#34A853',
    justifyContent: 'center',
    alignItems: 'center',
  },
  summaryCard: {
    flexDirection: 'row',
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 16,
    marginBottom: 32,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  summaryItem: { flex: 1, alignItems: 'center' },
  summaryNum: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  summaryLbl: { fontSize: 10, color: '#999', marginTop: 4, fontWeight: 'bold' },
  summaryDivider: { width: 1, height: 24, backgroundColor: '#F0F0F0', alignSelf: 'center' },
  agendaHead: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  kickerSmall: { fontSize: 10, fontWeight: 'bold', color: '#999', letterSpacing: 1 },
  agendaTitle: { fontSize: 18, fontWeight: 'bold', color: '#333', marginTop: 4 },
  listBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 12,
  },
  listBtnText: { fontSize: 12, fontWeight: 'bold', color: '#333' },
  agendaCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  timeBoxLarge: {
    width: 70,
    height: 60,
    backgroundColor: '#F0F0F0',
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  timeTxtLarge: { fontSize: 18, fontWeight: 'bold', color: '#34A853' },
  durTxtSmall: { fontSize: 10, color: '#999', marginTop: 2 },
  agendaNameLarge: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  locationRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    marginTop: 4,
  },
  agendaMetaSmall: { fontSize: 12, color: '#999' },
  onlineBadge: {
    backgroundColor: '#E8F5E9',
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderRadius: 6,
    marginLeft: 8,
  },
  onlineBadgeText: { fontSize: 8, fontWeight: 'bold', color: '#34A853' },
  tutorRowSmall: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
  },
  avatarTiny: { width: 20, height: 20, borderRadius: 10 },
  tutorPillSmall: {
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 8,
  },
  tutorPillText: { fontSize: 10, color: '#333', fontWeight: 'bold' },
  detailsBtn: {
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 12,
  },
  detailsBtnText: { fontSize: 10, fontWeight: 'bold', color: '#fff' },
  noMoreBox: {
    alignItems: 'center',
    paddingVertical: 40,
  },
  noMoreText: {
    fontSize: 14,
    color: '#999',
    marginBottom: 12,
  },
  browseLink: {
    fontSize: 14,
    color: '#34A853',
    fontWeight: 'bold',
  },
  fabYellow: {
    position: 'absolute',
    bottom: 20,
    right: 20,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: '#FFD700',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#FFD700',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 6,
  },
  timeBox: {
    width: 60,
    height: 40,
    backgroundColor: '#F0F0F0',
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  timeTxt: { fontSize: 12, fontWeight: 'bold', color: '#34A853' },
  agendaName: { fontSize: 16, fontWeight: 'bold', color: '#333' },
  agendaMeta: { fontSize: 12, color: '#999', marginTop: 4 },
  joinBtn: {
    backgroundColor: '#34A853',
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 10,
  },
  joinBtnText: { fontSize: 10, fontWeight: 'bold', color: '#fff' },
  emptyBox: { alignItems: 'center', paddingVertical: 40 },
  emptyText: { fontSize: 14, color: '#999', marginBottom: 12 },
  emptyCta: { fontSize: 14, color: '#34A853', fontWeight: 'bold' },
});
