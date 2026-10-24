import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  TouchableOpacity,
} from 'react-native';
import { useAuth } from '../../context/AuthContext';
import api from '../../services/api';

import { MaterialCommunityIcons } from '@expo/vector-icons';
import { tutoriaService, tutorService } from '../../services/api';

export default function TutorHomeScreen({ navigation }) {
  const { user } = useAuth();
  const [stats, setStats] = useState({ tutorias: 0, pendientes: 0, completadas: 0, rating: 4.9, hours: 0 });
  const [refreshing, setRefreshing] = useState(false);
  const [available, setAvailable] = useState(true);
  const [upcoming, setUpcoming] = useState([]);

  async function loadData() {
    try {
      const [profileRes, tutoriasRes] = await Promise.all([
        tutorService.miPerfil(),
        tutoriaService.getMisTutoriasComoTutor({ page_size: 5 })
      ]);
      
      const p = profileRes.data;
      setStats({
        tutorias: p.total_tutorias || 0,
        pendientes: 0, // We'll calculate from tutoriasRes if needed
        completadas: 0, 
        rating: p.calificacion || 5.0,
        hours: Math.floor((p.total_tutorias || 0) * 1.5)
      });
      setAvailable(p.disponible);

      const tList = tutoriasRes.data?.results || tutoriasRes.data || [];
      setUpcoming(tList.filter(t => t.estado === 'pendiente').slice(0, 3));
    } catch (error) {
      console.error('Error loading tutor data:', error);
    }
  }

  useEffect(() => {
    loadData();
  }, []);

  async function toggleAvailability() {
    try {
      // Toggle logic using tutorService if available or direct api
      setAvailable(!available);
    } catch (error) {
      console.error('Error toggling availability:', error);
    }
  }

  function onRefresh() {
    setRefreshing(true);
    loadData().finally(() => setRefreshing(false));
  }

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      <View style={styles.header}>
        <Text style={styles.welcomeKicker}>BIENVENIDO DE NUEVO,</Text>
        <Text style={styles.welcomeName}>Profesor {user?.first_name || user?.username || 'Tutor'}</Text>
        <Text style={styles.subtitle}>La excelencia académica empieza con tu guía.</Text>
      </View>

      <View style={styles.availabilityRow}>
        <View style={styles.availabilityToggle}>
          <TouchableOpacity 
            style={[styles.toggleTrack, available && styles.toggleTrackActive]} 
            onPress={toggleAvailability}
            activeOpacity={0.8}
          >
            <View style={[styles.toggleThumb, available && styles.toggleThumbActive]} />
          </TouchableOpacity>
          <Text style={styles.availabilityText}>{available ? 'Disponible para tutorías' : 'No disponible'}</Text>
        </View>
        <MaterialCommunityIcons name="bell-outline" size={24} color="#333" />
      </View>

      <View style={styles.statsGrid}>
        <View style={styles.statCard}>
          <View style={styles.statIconRow}>
            <MaterialCommunityIcons name="school-outline" size={24} color="#34A853" />
            <Text style={styles.statBadge}>TOTAL</Text>
          </View>
          <Text style={styles.statNumber}>{stats.tutorias}</Text>
          <Text style={styles.statLabel}>Tutorías realizadas</Text>
        </View>

        <View style={[styles.statCard, { backgroundColor: '#006D32' }]}>
          <MaterialCommunityIcons name="timer-outline" size={24} color="#fff" />
          <Text style={[styles.statNumber, { color: '#fff', marginTop: 12 }]}>{stats.hours}</Text>
          <Text style={[styles.statLabel, { color: 'rgba(255,255,255,0.7)' }]}>Horas totales de enseñanza</Text>
        </View>

        <View style={styles.statCard}>
          <View style={styles.statIconRow}>
            <MaterialCommunityIcons name="star-outline" size={24} color="#B8860B" />
            <View style={styles.starsRow}>
              {[1, 2, 3, 4, 5].map((s) => (
                <MaterialCommunityIcons key={s} name="star" size={10} color={s <= Math.round(stats.rating) ? "#B8860B" : "#DDD"} />
              ))}
            </View>
          </View>
          <Text style={styles.statNumber}>{Number(stats.rating).toFixed(1)}</Text>
          <Text style={styles.statLabel}>Calificación promedio</Text>
        </View>
      </View>

      <View style={styles.sectionHead}>
        <Text style={styles.sectionTitle}>Próximas sesiones</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Tutorias')}>
          <Text style={styles.link}>Ver calendario</Text>
        </TouchableOpacity>
      </View>

      {upcoming.length === 0 ? (
        <Text style={styles.emptyHint}>No tienes sesiones próximas.</Text>
      ) : (
        upcoming.map((item) => {
          const d = item.fecha_inicio ? new Date(item.fecha_inicio) : null;
          const dateStr = d ? d.toLocaleDateString('es-CO', { month: 'short', day: 'numeric', year: 'numeric' }) : '—';
          const timeStr = d ? d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', hour12: false }) : '—';

          return (
            <View key={item.id} style={styles.sessionCard}>
              <View style={styles.sessionCardTop}>
                <View style={styles.studentAvatar} />
                <View style={{ flex: 1, marginLeft: 12 }}>
                  <Text style={styles.studentName}>{item.estudiante_nombre || 'Estudiante'}</Text>
                  <Text style={styles.subjectTag}>{item.materia_nombre?.toUpperCase() || 'MATERIA'}</Text>
                </View>
                <View style={styles.dateTimeBox}>
                  <Text style={styles.sessionDate}>{dateStr}</Text>
                  <Text style={styles.sessionTime}>{timeStr}</Text>
                </View>
              </View>
              <View style={styles.sessionCardBtns}>
                <TouchableOpacity style={styles.rescheduleBtn}>
                  <Text style={styles.rescheduleBtnText}>Reprogramar</Text>
                </TouchableOpacity>
                <TouchableOpacity style={styles.startBtn} onPress={() => navigation.navigate('Tutorias')}>
                  <Text style={styles.startBtnText}>Ver sesión</Text>
                </TouchableOpacity>
              </View>
            </View>
          );
        })
      )}

      <View style={styles.helpCenter}>
        <View style={styles.helpTextContainer}>
          <Text style={styles.helpTitle}>Centro de ayuda para tutores</Text>
          <Text style={styles.helpDesc}>
            Consulta recursos pedagógicos, resuelve tus dudas o habla con el asistente de TutoUdec.
          </Text>
          <TouchableOpacity style={styles.helpBtn}>
            <Text style={styles.helpBtnText}>Obtener ayuda →</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.helpIconBox}>
          <MaterialCommunityIcons name="lightbulb-on-outline" size={40} color="rgba(255,255,255,0.3)" />
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  content: { padding: 20, paddingBottom: 120 },
  header: { marginTop: 40, marginBottom: 24 },
  welcomeKicker: { fontSize: 12, fontWeight: 'bold', color: '#999', letterSpacing: 1 },
  welcomeName: { fontSize: 28, fontWeight: 'bold', color: '#333', marginTop: 4 },
  subtitle: { fontSize: 14, color: '#666', marginTop: 8 },
  availabilityRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 32,
  },
  availabilityToggle: { flexDirection: 'row', alignItems: 'center' },
  toggleTrack: {
    width: 50,
    height: 28,
    borderRadius: 14,
    backgroundColor: '#EEE',
    padding: 2,
    marginRight: 12,
  },
  toggleTrackActive: { backgroundColor: '#34A853' },
  toggleThumb: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: '#fff',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.2,
    shadowRadius: 2,
    elevation: 2,
  },
  toggleThumbActive: { transform: [{ translateX: 22 }] },
  availabilityText: { fontSize: 14, fontWeight: '600', color: '#333' },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 32,
  },
  statCard: {
    flex: 1,
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 16,
    marginHorizontal: 4,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  statIconRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  statBadge: {
    fontSize: 8,
    fontWeight: 'bold',
    color: '#34A853',
  },
  starsRow: {
    flexDirection: 'row',
  },
  statNumber: { fontSize: 24, fontWeight: 'bold', color: '#333' },
  statLabel: { fontSize: 10, color: '#999', marginTop: 4 },
  sectionHead: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  link: { fontSize: 14, fontWeight: '600', color: '#34A853' },
  sessionCard: {
    backgroundColor: '#F9F9F9',
    borderRadius: 20,
    padding: 16,
    marginBottom: 16,
  },
  sessionCardTop: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  studentAvatar: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: '#A5D6A7',
  },
  studentName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
  },
  subjectTag: {
    fontSize: 10,
    fontWeight: 'bold',
    color: '#34A853',
    marginTop: 4,
  },
  dateTimeBox: {
    alignItems: 'flex-end',
  },
  sessionDate: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#333',
  },
  sessionTime: {
    fontSize: 10,
    color: '#999',
    marginTop: 4,
  },
  sessionCardBtns: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 16,
  },
  rescheduleBtn: {
    flex: 1,
    backgroundColor: '#fff',
    borderWidth: 1,
    borderColor: '#DDD',
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: 'center',
    marginRight: 8,
  },
  rescheduleBtnText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
  },
  startBtn: {
    flex: 1,
    backgroundColor: '#006D32',
    borderRadius: 12,
    paddingVertical: 12,
    alignItems: 'center',
    marginLeft: 8,
  },
  startBtnText: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#fff',
  },
  emptyHint: { fontSize: 14, color: '#999', fontStyle: 'italic', marginVertical: 12, textAlign: 'center' },
  helpCenter: {
    backgroundColor: '#004D40',
    borderRadius: 24,
    padding: 24,
    flexDirection: 'row',
    alignItems: 'center',
    overflow: 'hidden',
  },
  helpTextContainer: { flex: 1, zIndex: 1 },
  helpTitle: { color: '#fff', fontSize: 20, fontWeight: 'bold', marginBottom: 8 },
  helpDesc: { color: 'rgba(255,255,255,0.7)', fontSize: 12, lineHeight: 18, marginBottom: 16 },
  helpBtn: { flexDirection: 'row', alignItems: 'center' },
  helpBtnText: { color: '#fff', fontSize: 14, fontWeight: 'bold' },
  helpIconBox: { position: 'absolute', right: -10, bottom: -10 },
});