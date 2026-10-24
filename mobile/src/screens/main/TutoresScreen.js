import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TextInput,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import AppHeader from '../../components/AppHeader';
import { tutorService } from '../../services/api';
import { C } from '../../theme/colors';

const AVATAR =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuDEejO4pSWu1w_8uNMBI6ZJJsnoS3zuBgAnYOXP9z8A7tRg-rX-lAPTWwonxjtiEVgWXmxFJ7hIGPhH0HuC6XeA2GvTlyNzHUXszNB2br0wHj8lGYKUcf2fnwsM_I_oxFERjZT-pZvKfdszh9BmtI3vnW2ikhv4bL6AIklRomWHXkhqRFtNMh-lnJjAbennxCj_M6Lm7am_W24UjgrJY6VbM4Pr0caYWCq8RufJwrlTlBmKtE0gAx586JmQQOtfIQsm6oltra19LRM';

function listPayload(data) {
  if (!data) return [];
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.results)) return data.results;
  return [];
}

export default function TutoresScreen({ navigation, route }) {
  const [query, setQuery] = useState(route.params?.initialQuery ?? '');
  const [tutores, setTutores] = useState([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    if (route.params?.initialQuery != null) {
      setQuery(route.params.initialQuery);
    }
  }, [route.params?.initialQuery]);

  const fetchList = async (q) => {
    const params = { page_size: 40 };
    const term = String(q ?? '').trim();
    if (term) params.search = term;
    const { data } = await tutorService.getAll(params);
    return listPayload(data);
  };

  useEffect(() => {
    let alive = true;
    const t = setTimeout(async () => {
      setLoading(true);
      try {
        const list = await fetchList(query);
        if (alive) setTutores(list);
      } catch (e) {
        if (alive) setTutores([]);
      } finally {
        if (alive) setLoading(false);
      }
    }, 320);
    return () => {
      alive = false;
      clearTimeout(t);
    };
  }, [query]);

  const onRefresh = async () => {
    setRefreshing(true);
    try {
      setTutores(await fetchList(query));
    } catch {
      setTutores([]);
    } finally {
      setRefreshing(false);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.cardTop}>
        <View style={styles.avatarBox}>
          <View style={styles.photoPlaceholderLarge}>
            <MaterialCommunityIcons name="account" size={60} color="#DDD" />
          </View>
          <View style={[styles.statusDot, { backgroundColor: item.disponible ? '#22C55E' : '#999' }]} />
        </View>
        <View style={styles.infoBox}>
          <View style={styles.nameRow}>
            <Text style={styles.tutorNameLarge}>{item.usuario_nombre || 'Tutor'}</Text>
            <View style={styles.ratingBoxSmall}>
              <MaterialCommunityIcons name="star" size={12} color="#FBC02D" />
              <Text style={styles.ratingTextSmall}>{Number(item.calificacion ?? 0).toFixed(1)}</Text>
            </View>
          </View>
          <Text style={styles.specialtyText}>{item.especialidad || 'Tutor general'}</Text>
          <Text style={styles.bioText} numberOfLines={3}>
            {item.bio || 'Este tutor aún no ha agregado una descripción.'}
          </Text>
          <View style={styles.tagRowLarge}>
            {(item.materias_nombres || []).slice(0, 2).map((n) => (
              <View key={n} style={styles.tagPill}><Text style={styles.tagPillText}>{n}</Text></View>
            ))}
            <View style={[styles.tagPill, { backgroundColor: '#F0F0F0' }]}>
              <Text style={[styles.tagPillText, { color: '#666' }]}>${Number(item.tarifa_por_hora ?? 0).toLocaleString('es-CO')}/h</Text>
            </View>
          </View>
        </View>
      </View>
      <TouchableOpacity 
        style={styles.viewProfileBtnLarge} 
        activeOpacity={0.9}
        onPress={() => navigation.navigate('TutorDetail', { tutorId: item.id })}
      >
        <Text style={styles.viewProfileBtnTextLarge}>Ver perfil</Text>
      </TouchableOpacity>
    </View>
  );

  return (
    <View style={styles.root}>
      <AppHeader
        variant="home"
        avatarUri={AVATAR}
        onPressAvatar={() => navigation.navigate('Profile')}
        onPressBell={() => {}}
      />

      <Text style={styles.h2}>Encuentra tu tutor</Text>

      <View style={styles.searchWrap}>
        <MaterialCommunityIcons name="magnify" size={22} color="#999" style={{ marginLeft: 16 }} />
        <TextInput
          style={styles.searchInput}
          placeholder="Materia, nombre..."
          placeholderTextColor="#999"
          value={query}
          onChangeText={setQuery}
          returnKeyType="search"
        />
      </View>

      <View style={styles.chips}>
        <View style={styles.chipPrimary}>
          <Text style={styles.chipPrimaryText}>{query.trim() || 'Todos'}</Text>
          {query.trim() ? (
            <TouchableOpacity onPress={() => setQuery('')}>
              <MaterialCommunityIcons name="close" size={18} color="#fff" />
            </TouchableOpacity>
          ) : null}
        </View>
        <TouchableOpacity style={styles.chipGhost} onPress={() => navigation.navigate('Materias')}>
          <MaterialCommunityIcons name="filter-variant" size={18} color="#666" />
          <Text style={styles.chipGhostText}>Materias</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.countRow}>
        <Text style={styles.count}>{tutores.length} TUTORES DISPONIBLES</Text>
        <Text style={styles.sort}>Orden: mejor calificados</Text>
      </View>

      {loading && tutores.length === 0 ? (
        <ActivityIndicator style={{ marginTop: 24 }} color="#34A853" />
      ) : (
        <FlatList
          data={tutores}
          keyExtractor={(item) => String(item.id)}
          renderItem={renderItem}
          contentContainerStyle={{ paddingBottom: 100 }}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
          ListEmptyComponent={
            <Text style={styles.empty}>No se encontraron tutores. Prueba otra búsqueda.</Text>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  root: { flex: 1, backgroundColor: '#fff', paddingHorizontal: 20 },
  h2: { fontSize: 24, fontWeight: 'bold', color: '#333', marginBottom: 16, marginTop: 8 },
  searchWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
    borderRadius: 20,
    height: 56,
    marginBottom: 16,
  },
  searchInput: { flex: 1, paddingHorizontal: 12, fontSize: 16, color: '#333' },
  chips: { flexDirection: 'row', gap: 8, marginBottom: 24, flexWrap: 'wrap' },
  chipPrimary: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#006D32',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 12,
  },
  chipPrimaryText: { color: '#fff', fontWeight: 'bold', fontSize: 14 },
  chipGhost: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 6,
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 16,
    paddingVertical: 10,
    borderRadius: 12,
  },
  chipGhostText: { color: '#666', fontWeight: '600', fontSize: 14 },
  countRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  count: { fontSize: 12, fontWeight: 'bold', color: '#999' },
  sort: { fontSize: 12, color: '#34A853', fontWeight: '600' },
  card: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 20,
    marginBottom: 20,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  cardTop: { flexDirection: 'row', gap: 20 },
  avatarBox: { width: 80, alignItems: 'center' },
  photoPlaceholderLarge: {
    width: 80,
    height: 100,
    borderRadius: 16,
    backgroundColor: '#F0F0F0',
    justifyContent: 'center',
    alignItems: 'center',
  },
  statusDot: {
    width: 14,
    height: 14,
    borderRadius: 7,
    borderWidth: 2,
    borderColor: '#fff',
    position: 'absolute',
    bottom: -4,
    right: 4,
  },
  infoBox: { flex: 1 },
  nameRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 },
  tutorNameLarge: { fontSize: 18, fontWeight: 'bold', color: '#333' },
  ratingBoxSmall: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
    backgroundColor: '#FFF9C4',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 10,
  },
  ratingTextSmall: { fontSize: 12, fontWeight: 'bold', color: '#FBC02D' },
  specialtyText: { fontSize: 14, color: '#34A853', fontWeight: '600', marginBottom: 8 },
  bioText: { fontSize: 12, color: '#999', lineHeight: 18, marginBottom: 12 },
  tagRowLarge: { flexDirection: 'row', gap: 8 },
  tagPill: { backgroundColor: '#E8F5E9', paddingHorizontal: 12, paddingVertical: 6, borderRadius: 8 },
  tagPillText: { fontSize: 10, fontWeight: 'bold', color: '#34A853' },
  viewProfileBtnLarge: {
    marginTop: 20,
    backgroundColor: '#006D32',
    paddingVertical: 14,
    borderRadius: 30,
    alignItems: 'center',
  },
  viewProfileBtnTextLarge: { color: '#fff', fontSize: 16, fontWeight: 'bold' },
  empty: { textAlign: 'center', marginTop: 40, color: '#999', fontSize: 14 },
});
