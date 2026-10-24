import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
  RefreshControl,
  FlatList,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { materiaService, tutorService } from '../../services/api';
import { C } from '../../theme/colors';

export default function MateriaDetailScreen({ route, navigation }) {
  const { materiaId } = route.params;
  const [materia, setMateria] = useState(null);
  const [tutores, setTutores] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const [materiaRes, tutoresRes] = await Promise.all([
        materiaService.getById(materiaId),
        materiaService.getTutores(materiaId),
      ]);
      
      setMateria(materiaRes.data);
      setTutores(Array.isArray(tutoresRes.data) ? tutoresRes.data : []);
    } catch (error) {
      console.error('Error loading materia:', error);
      Alert.alert('Error', 'No se pudo cargar la información de la materia');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [materiaId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const onRefresh = async () => {
    setRefreshing(true);
    await loadData();
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#34A853" />
        <Text style={styles.loadingText}>Cargando...</Text>
      </View>
    );
  }

  if (!materia) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>No se encontró la materia</Text>
        <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
          <Text style={styles.backButtonText}>Volver</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <MaterialCommunityIcons name="arrow-left" size={24} color="#34A853" />
        </TouchableOpacity>
        <View style={{ flex: 1 }}>
          <Text style={styles.headerTitle} numberOfLines={1}>{materia.nombre}</Text>
        </View>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView
        style={styles.scroll}
        contentContainerStyle={styles.content}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
      >
        <View style={styles.materiaCard}>
          <View style={styles.materiaIcon}>
            <Text style={styles.materiaIconText}>{materia.nombre.charAt(0)}</Text>
          </View>
          <Text style={styles.materiaNombre}>{materia.nombre}</Text>
          {materia.descripcion && (
            <Text style={styles.materiaDescripcion}>{materia.descripcion}</Text>
          )}
          <View style={styles.statsRow}>
            <View style={styles.stat}>
              <MaterialCommunityIcons name="book-open" size={20} color="#34A853" />
              <Text style={styles.statText}>{tutores.length} tutores</Text>
            </View>
            <View style={styles.stat}>
              <MaterialCommunityIcons name="star" size={20} color="#FBC02D" />
              <Text style={styles.statText}>{Number(materia.valoracion ?? 0).toFixed(1)} valoración</Text>
            </View>
          </View>
        </View>

        <View style={styles.sectionHead}>
          <Text style={styles.sectionTitle}>Tutores disponibles</Text>
        </View>

        {tutores.length === 0 ? (
          <View style={styles.emptyContainer}>
            <MaterialCommunityIcons name="account-off" size={64} color="#ccc" />
            <Text style={styles.emptyText}>No hay tutores disponibles para esta materia</Text>
          </View>
        ) : (
          tutores.map((tutor) => (
            <TouchableOpacity
              key={tutor.id}
              style={styles.tutorCard}
              activeOpacity={0.9}
              onPress={() => navigation.navigate('TutorDetail', { tutorId: tutor.id })}
            >
              <View style={styles.tutorAvatar}>
                <MaterialCommunityIcons name="account" size={28} color={C.primary} />
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.tutorName}>{tutor.usuario_nombre || 'Tutor'}</Text>
                <Text style={styles.tutorEspecialidad}>{tutor.especialidad || 'General'}</Text>
                <View style={styles.starRow}>
                  <MaterialCommunityIcons name="star" size={16} color="#FBC02D" />
                  <Text style={styles.starText}>
                    {Number(tutor.calificacion ?? 0).toFixed(1)}
                  </Text>
                  <Text style={styles.tarifaText}>
                    ${Number(tutor.tarifa_por_hora ?? 0).toLocaleString('es-CO')}/hora
                  </Text>
                </View>
              </View>
              <View style={styles.nivelBadge}>
                <Text style={styles.nivelText}>{tutor.nivel_experiencia || 'intermedio'}</Text>
              </View>
            </TouchableOpacity>
          ))
        )}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  loadingText: {
    fontSize: 16,
    color: '#666',
    marginTop: 16,
  },
  backButton: {
    marginTop: 24,
    backgroundColor: '#34A853',
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 12,
  },
  backButtonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingTop: 50,
    paddingBottom: 15,
    paddingHorizontal: 20,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#f0f0f0',
  },
  backBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    textAlign: 'center',
  },
  scroll: {
    flex: 1,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  materiaCard: {
    backgroundColor: '#34A853',
    borderRadius: 24,
    padding: 24,
    alignItems: 'center',
    marginBottom: 32,
  },
  materiaIcon: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: 'rgba(255,255,255,0.2)',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  materiaIconText: {
    fontSize: 36,
    fontWeight: 'bold',
    color: '#fff',
  },
  materiaNombre: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#fff',
    textAlign: 'center',
    marginBottom: 8,
  },
  materiaDescripcion: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.8)',
    textAlign: 'center',
    lineHeight: 20,
    marginBottom: 16,
  },
  statsRow: {
    flexDirection: 'row',
    gap: 24,
  },
  stat: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  statText: {
    color: '#fff',
    fontSize: 14,
    fontWeight: '600',
  },
  sectionHead: {
    marginBottom: 16,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
  },
  emptyContainer: {
    alignItems: 'center',
    paddingVertical: 48,
  },
  emptyText: {
    fontSize: 16,
    color: '#999',
    marginTop: 16,
    textAlign: 'center',
  },
  tutorCard: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#F0F0F0',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.05,
    shadowRadius: 10,
    elevation: 2,
  },
  tutorAvatar: {
    width: 56,
    height: 56,
    borderRadius: 20,
    backgroundColor: '#E8F5E9',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  tutorName: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 4,
  },
  tutorEspecialidad: {
    fontSize: 12,
    color: '#666',
    marginBottom: 4,
  },
  starRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 4,
  },
  starText: {
    fontSize: 14,
    color: '#333',
    fontWeight: '600',
  },
  tarifaText: {
    fontSize: 14,
    color: '#34A853',
    fontWeight: 'bold',
    marginLeft: 8,
  },
  nivelBadge: {
    backgroundColor: '#F0F0F0',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 8,
  },
  nivelText: {
    fontSize: 10,
    fontWeight: 'bold',
    color: '#666',
  },
});
