import React, { useState, useEffect, useMemo } from 'react';
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
import { materiaService } from '../../services/api';
import { C } from '../../theme/colors';

const MateriasScreen = ({ navigation }) => {
  const [materias, setMaterias] = useState([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadMaterias = async () => {
    try {
      const response = await materiaService.getAll({ page_size: 100 });
      setMaterias(response.data.results || response.data);
    } catch (error) {
      console.error('Error cargando materias:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await loadMaterias();
    setRefreshing(false);
  };

  useEffect(() => {
    loadMaterias();
  }, []);

  const filtradas = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return materias;
    return materias.filter(
      (m) => m.nombre?.toLowerCase().includes(q) || m.descripcion?.toLowerCase().includes(q)
    );
  }, [materias, query]);

  const renderMateria = ({ item }) => (
    <View style={styles.card}>
      <View style={styles.cardTop}>
        <View style={styles.iconBox}>
          <MaterialCommunityIcons name="book-open-variant" size={44} color="#34A853" />
        </View>
        <View style={styles.infoBox}>
          <View style={styles.nameRow}>
            <Text style={styles.name} numberOfLines={2}>{item.nombre}</Text>
            <View style={styles.ratingBox}>
              <MaterialCommunityIcons name="star" size={12} color="#FBC02D" />
              <Text style={styles.ratingText}>{Number(item.valoracion ?? 0).toFixed(1)}</Text>
            </View>
          </View>
          <Text style={styles.descText} numberOfLines={3}>
            {item.descripcion || 'Esta materia aún no tiene descripción.'}
          </Text>
          <View style={styles.tagRow}>
            <View style={styles.tagPill}>
              <Text style={styles.tagPillText}>{item.total_tutores ?? 0} tutores</Text>
            </View>
            <View style={[styles.tagPill, { backgroundColor: '#F0F0F0' }]}>
              <Text style={[styles.tagPillText, { color: '#666' }]}>{item.total_tutorias ?? 0} tutorías</Text>
            </View>
          </View>
        </View>
      </View>
      <TouchableOpacity
        style={styles.viewBtn}
        activeOpacity={0.9}
        onPress={() => navigation.navigate('MateriaDetail', { materiaId: item.id })}
      >
        <Text style={styles.viewBtnText}>Ver materia</Text>
      </TouchableOpacity>
    </View>
  );

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={C.primaryContainer} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <AppHeader
        variant="stack"
        left={
          <TouchableOpacity
            onPress={() =>
              navigation.canGoBack() ? navigation.goBack() : navigation.navigate('Home')
            }
            style={styles.backBtn}
          >
            <MaterialCommunityIcons name="arrow-left" size={22} color={C.onSurface} />
          </TouchableOpacity>
        }
        right={<View />}
      />
      <FlatList
        style={styles.listFlex}
        data={filtradas}
        renderItem={renderMateria}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
        ListEmptyComponent={<Text style={styles.empty}>No hay materias disponibles</Text>}
        ListHeaderComponent={
          <View>
            <Text style={styles.pageTitle}>Materias</Text>
            <View style={styles.searchWrap}>
              <MaterialCommunityIcons name="magnify" size={22} color="#999" style={{ marginLeft: 16 }} />
              <TextInput
                style={styles.searchInput}
                placeholder="Buscar materia..."
                placeholderTextColor="#999"
                value={query}
                onChangeText={setQuery}
              />
            </View>
            <Text style={styles.count}>{filtradas.length} MATERIAS</Text>
          </View>
        }
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#fff' },
  listFlex: { flex: 1 },
  backBtn: { width: 40, height: 40, alignItems: 'center', justifyContent: 'center' },
  pageTitle: { fontSize: 24, fontWeight: 'bold', color: '#333', marginBottom: 16, marginTop: 8 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  list: { paddingHorizontal: 20, paddingBottom: 100 },
  searchWrap: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
    borderRadius: 20,
    height: 56,
    marginBottom: 16,
  },
  searchInput: { flex: 1, paddingHorizontal: 12, fontSize: 16, color: '#333' },
  count: { fontSize: 12, fontWeight: 'bold', color: '#666', marginBottom: 12, letterSpacing: 1 },
  card: {
    backgroundColor: '#fff',
    borderRadius: 24,
    padding: 16,
    marginBottom: 16,
    borderWidth: 1,
    borderColor: '#EEE',
    elevation: 2,
    shadowColor: '#000',
    shadowOpacity: 0.06,
    shadowRadius: 8,
    shadowOffset: { width: 0, height: 2 },
  },
  cardTop: { flexDirection: 'row', gap: 14 },
  iconBox: {
    width: 84,
    height: 84,
    borderRadius: 20,
    backgroundColor: '#E8F5E9',
    alignItems: 'center',
    justifyContent: 'center',
  },
  infoBox: { flex: 1 },
  nameRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8 },
  name: { flex: 1, fontSize: 17, fontWeight: 'bold', color: '#333' },
  ratingBox: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 3,
    backgroundColor: '#FFF8E1',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
  },
  ratingText: { fontSize: 12, fontWeight: 'bold', color: '#333' },
  descText: { fontSize: 13, color: '#666', marginTop: 6, lineHeight: 18 },
  tagRow: { flexDirection: 'row', gap: 6, marginTop: 10, flexWrap: 'wrap' },
  tagPill: { backgroundColor: '#E8F5E9', paddingHorizontal: 10, paddingVertical: 4, borderRadius: 10 },
  tagPillText: { fontSize: 11, fontWeight: 'bold', color: '#006D32' },
  viewBtn: {
    marginTop: 14,
    backgroundColor: '#006D32',
    borderRadius: 16,
    paddingVertical: 14,
    alignItems: 'center',
  },
  viewBtnText: { color: '#fff', fontWeight: 'bold', fontSize: 15 },
  empty: { textAlign: 'center', color: '#666', marginTop: 50, fontSize: 16 },
});

export default MateriasScreen;
