import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  FlatList,
  TextInput,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AppHeader from '../../components/AppHeader';
import { useAuth } from '../../context/AuthContext';
import { tutorService, materiaService, tutoriaService } from '../../services/api';
import { C } from '../../theme/colors';

const STUDENT_AVATAR =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDVcwn6s4nV1CHSNpmpipBJK0bu9UNLelccnDqAHqmn7QUlTePVc_DbrcM_JX2z9MgKGXvfnI2AzQG0IEvmbYFSUI6AfERimpAo9FkFyHLLAXKw0x7OBblhNYt4i2vJhIq_rZMEi3IPzG0MRpxEZBH7m-prN9iibsqFPtjwwEcTMUY_KfpEt5xgXYOU-KXKYE_q_W7YI7YUjPLUgCvD5qa5vaoPbh0MN5JNhYetwk78LyAkMZ9GzqGpSWEPAEnTSyP_w4l1KUi3KGw';

function listPayload(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}

export default function HomeScreen({ navigation }) {
  const { user } = useAuth();
  const displayName =
    [user?.first_name, user?.last_name].filter(Boolean).join(' ') || user?.username || 'Estudiante';

  const [search, setSearch] = useState('');
  const [materias, setMaterias] = useState([]);
  const [tutores, setTutores] = useState([]);
  const [upcoming, setUpcoming] = useState([]);
  const [refreshing, setRefreshing] = useState(false);

  const load = useCallback(async () => {
    try {
      const [mr, tr, tu] = await Promise.all([
        materiaService.getAll({ page_size: 10 }),
        tutorService.getAll({ page_size: 8 }),
        tutoriaService.getMisTutorias({ page_size: 20 }),
      ]);
      setMaterias(listPayload(mr.data));
      setTutores(listPayload(tr.data));
      const tList = listPayload(tu.data);
      const sorted = [...tList].sort(
        (a, b) => new Date(a.fecha_inicio) - new Date(b.fecha_inicio)
      );
      setUpcoming(sorted.slice(0, 3));
    } catch (e) {
      console.warn('Home load', e.message);
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

  const learningData = materias.slice(0, 5);

  return (
    <View style={styles.root}>
      <AppHeader
        variant="home"
        avatarUri={STUDENT_AVATAR}
        onPressAvatar={() => navigation.navigate('Profile')}
        onPressBell={() => {}}
      />
      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        showsVerticalScrollIndicator={false}
      >
      <View style={styles.welcomeRow}>
        <View style={{ flex: 1 }}>
          <Text style={styles.welcomeKicker}>BIENVENIDO DE NUEVO,</Text>
          <Text style={styles.welcomeName}>{displayName}!</Text>
        </View>
      </View>

      <View style={styles.searchWrap}>
        <MaterialCommunityIcons name="magnify" size={22} color={C.outline} style={styles.searchIcon} />
        <TextInput
          style={styles.searchInput}
          placeholder="Buscar materias o tutores..."
          placeholderTextColor={C.outline}
          value={search}
          onChangeText={setSearch}
          returnKeyType="search"
          onSubmitEditing={() => {
            navigation.navigate('Tutores', { initialQuery: search });
          }}
        />
      </View>

      <View style={styles.sectionHead}>
        <Text style={styles.sectionTitle}>Tu Ruta de Aprendizaje</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Materias')}>
          <Text style={styles.link}>Ver todo</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        horizontal
        data={learningData}
        keyExtractor={(item) => String(item.id)}
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={{ paddingRight: 8 }}
        renderItem={({ item, index }) => (
          <TouchableOpacity
            style={[
              styles.pathCard,
              { backgroundColor: index % 2 === 0 ? '#006D32' : '#34A853' },
              { marginRight: 12 },
            ]}
            onPress={() => navigation.navigate('Materias')}
            activeOpacity={0.9}
          >
            <View style={styles.pathCardTop}>
              <View style={styles.pathIcon}>
                <Text style={styles.pathIconText}>{item.nombre.charAt(0)}</Text>
              </View>
              <View style={styles.badgeActive}>
                <Text style={styles.badgeActiveText}>ACTIVO</Text>
              </View>
            </View>
            <Text style={styles.pathTitle} numberOfLines={2}>
              {item.nombre}
            </Text>
            <Text style={styles.pathSub}>
              {item.total_tutorias ?? 0} sesiones completadas
            </Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          <Text style={styles.emptyHint}>Carga materias desde el backend o revisa la conexión.</Text>
        }
      />

      <View style={styles.sectionHead}>
        <Text style={styles.sectionTitle}>Tus Próximas Tutorías</Text>
        <TouchableOpacity onPress={() => navigation.navigate('Tutorias')}>
          <Text style={styles.link}>Calendario</Text>
        </TouchableOpacity>
      </View>

      {upcoming.length === 0 ? (
        <Text style={styles.emptyHint}>No tienes sesiones próximas. Explora tutores.</Text>
      ) : (
        upcoming.map((t) => {
          const d = t.fecha_inicio ? new Date(t.fecha_inicio) : null;
          const mes = d
            ? d.toLocaleDateString('es-CO', { month: 'short' }).toUpperCase()
            : '—';
          const dia = d ? d.getDate() : '—';
          return (
            <TouchableOpacity
              key={t.id}
              style={styles.sessionRow}
              onPress={() => navigation.navigate('Tutorias')}
              activeOpacity={0.85}
            >
              <View style={styles.sessionDate}>
                <Text style={styles.sessionMes}>{mes}</Text>
                <Text style={styles.sessionDia}>{dia}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.sessionTitle}>{t.materia_nombre || 'Tutoría'}</Text>
                <Text style={styles.sessionMeta}>
                  {d ? d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', hour12: false }) : ''} - {t.duracion_minutos ? new Date(d.getTime() + t.duracion_minutos*60000).toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit', hour12: false }) : ''}
                </Text>
                <Text style={styles.sessionMeta}>
                  {t.lugar || 'En línea'}
                </Text>
              </View>
              <View style={{ alignItems: 'center', gap: 8 }}>
                <View style={styles.tutorAvatarSmall}>
                  <MaterialCommunityIcons name="account" size={16} color="#fff" />
                  <View style={styles.tutorBadge} />
                </View>
                <View style={[styles.smallBtn, { backgroundColor: '#006D32' }]}>
                  <Text style={styles.smallBtnText}>UNIRSE</Text>
                </View>
              </View>
            </TouchableOpacity>
          );
        })
      )}

      <View style={styles.helpCenter}>
        <View style={styles.helpTextContainer}>
          <Text style={styles.helpTitle}>Centro de Ayuda TutoUdec</Text>
          <Text style={styles.helpDesc}>
            Accede a recursos pedagógicos, gestiona tus métodos de pago o contacta soporte técnico para tu aula digital.
          </Text>
          <TouchableOpacity style={styles.helpBtn} onPress={() => navigation.navigate('Chatbot')}>
            <Text style={styles.helpBtnText}>Obtener ayuda →</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.helpIconBox}>
          <MaterialCommunityIcons name="lightbulb-on-outline" size={40} color="rgba(255,255,255,0.3)" />
        </View>
      </View>

      <View style={styles.sectionHead}>
        <Text style={styles.sectionTitle}>Tutores Mejor Calificados</Text>
      </View>
      {tutores.slice(0, 2).map((tutor) => (
        <TouchableOpacity
          key={tutor.id}
          style={styles.tutorCard}
          onPress={() => navigation.navigate('Tutores')}
          activeOpacity={0.9}
        >
          <View style={styles.tutorCardInner}>
            <View style={styles.tutorAvatar}>
              <MaterialCommunityIcons name="account" size={28} color={C.primary} />
            </View>
            <View style={{ flex: 1 }}>
              <Text style={styles.tutorName}>{tutor.usuario_nombre || 'Tutor'}</Text>
              <View style={styles.tagRow}>
                <View style={styles.tag}><Text style={styles.tagText}>MATE</Text></View>
                <View style={styles.tag}><Text style={styles.tagText}>ESTAD</Text></View>
              </View>
              <View style={styles.starRow}>
                <MaterialCommunityIcons name="star" size={16} color="#FBC02D" />
                <Text style={styles.starText}>
                  {Number(tutor.calificacion ?? 0).toFixed(1)} ({tutor.total_tutorias ?? 0} reseñas)
                </Text>
              </View>
            </View>
            <TouchableOpacity style={styles.viewProfileBtn}>
              <Text style={styles.viewProfileBtnText}>Ver Perfil</Text>
            </TouchableOpacity>
          </View>
        </TouchableOpacity>
      ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#fff' },
  scroll: { flex: 1 },
  content: { paddingBottom: 120, paddingHorizontal: 20 },
  welcomeRow: { marginTop: 20, marginBottom: 24 },
  welcomeKicker: { fontSize: 12, fontWeight: 'bold', color: '#999', letterSpacing: 1 },
  welcomeName: { fontSize: 28, fontWeight: 'bold', color: '#333', marginTop: 4 },
  searchWrap: {
    flexDirection: 'row',
    alignItems: 'center', 
    backgroundColor: '#F0F0F0',
    borderRadius: 20,
    height: 56,
    paddingHorizontal: 16,
    marginBottom: 32,
  },
  searchIcon: { marginRight: 12 },
  searchInput: { flex: 1, fontSize: 16, color: '#333' },
  sectionHead: {
    flexDirection: 'row', 
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
    marginTop: 8,
  },
  sectionTitle: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  link: { fontSize: 14, color: '#34A853', fontWeight: 'bold' },
  pathCard: {
    width: 160,
    height: 180,
    borderRadius: 24,
    padding: 20,
    justifyContent: 'space-between',
  },
  pathCardTop: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start' },
  pathIcon: {
    width: 40,
    height: 40, 
    borderRadius: 12,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center', 
    alignItems: 'center',
  },
  pathIconText: { color: '#fff', fontSize: 18, fontWeight: 'bold' },
  badgeActive: {
    backgroundColor: 'rgba(255,255,255,0.2)',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 6,
  },
  badgeActiveText: { color: '#fff', fontSize: 8, fontWeight: 'bold' },
  pathTitle: { color: '#fff', fontSize: 16, fontWeight: 'bold', marginTop: 12 },
  pathSub: { color: 'rgba(255,255,255,0.7)', fontSize: 10, marginTop: 4 },
  sessionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 16, 
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10, 
    elevation: 2,
  },
  sessionDate: {
    width: 50, 
    height: 60,
    backgroundColor: '#F0F0F0',
    borderRadius: 16,
    justifyContent: 'center', 
    alignItems: 'center', 
    marginRight: 16,
  },
  sessionMes: { fontSize: 10, fontWeight: 'bold', color: '#999' },
  sessionDia: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  sessionTitle: { fontSize: 16, fontWeight: 'bold', color: '#333', marginBottom: 4 },
  sessionMeta: { fontSize: 12, color: '#999' },
  tutorAvatarSmall: { width: 32, height: 32, borderRadius: 16, backgroundColor: '#34A853', justifyContent: 'center', alignItems: 'center' },
  tutorBadge: { width: 10, height: 10, borderRadius: 5, backgroundColor: '#FFD700', position: 'absolute', bottom: 0, right: 0, borderWidth: 2, borderColor: '#fff' },
  smallBtn: { paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  smallBtnText: { color: '#fff', fontSize: 10, fontWeight: 'bold' },
  helpCenter: {
    flexDirection: 'row', 
    backgroundColor: '#006D32',
    borderRadius: 24,
    padding: 24,
    marginTop: 16,
    marginBottom: 32,
    overflow: 'hidden',
  },
  helpTextContainer: { flex: 1, zIndex: 1 },
  helpTitle: { color: '#fff', fontSize: 18, fontWeight: 'bold', marginBottom: 8 },
  helpDesc: { color: 'rgba(255,255,255,0.7)', fontSize: 12, lineHeight: 18, marginBottom: 16 },
  helpBtn: { backgroundColor: '#fff', paddingHorizontal: 16, paddingVertical: 10, borderRadius: 12, alignSelf: 'flex-start' },
  helpBtnText: { color: '#006D32', fontSize: 12, fontWeight: 'bold' },
  helpIconBox: { position: 'absolute', right: -10, bottom: -10 },
  tutorCard: { marginBottom: 16 },
  tutorCardInner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 16,
    borderWidth: 1,
    borderColor: '#F0F0F0',
  },
  tutorAvatar: { width: 56, height: 56, borderRadius: 20, backgroundColor: '#E8F5E9', justifyContent: 'center', alignItems: 'center', marginRight: 16 },
  tutorName: { fontSize: 16, fontWeight: 'bold', color: '#333', marginBottom: 4 },
  tagRow: { flexDirection: 'row', gap: 6, marginBottom: 6 },
  tag: { backgroundColor: '#F0F0F0', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  tagText: { fontSize: 8, fontWeight: 'bold', color: '#666' },
  starRow: { flexDirection: 'row', alignItems: 'center', gap: 4 },
  starText: { fontSize: 12, color: '#999', fontWeight: '600' },
  viewProfileBtn: { backgroundColor: '#F0F0F0', paddingHorizontal: 12, paddingVertical: 8, borderRadius: 12 },
  viewProfileBtnText: { fontSize: 10, fontWeight: 'bold', color: '#333' },
  emptyHint: { fontSize: 14, color: '#999', fontStyle: 'italic', marginVertical: 12 },
});
