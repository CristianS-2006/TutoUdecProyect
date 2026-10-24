import React, { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  Alert,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { C } from '../../theme/colors';
import { authService } from '../../services/api';

function apiMessage(error, fallback) {
  const data = error?.response?.data;
  if (data?.detail) return String(data.detail);
  if (error?.message === 'Network Error') return 'Sin conexión con el servidor.';
  return fallback;
}

export default function ForgotPasswordScreen({ navigation }) {
  const [step, setStep] = useState(1);
  const [email, setEmail] = useState('');
  const [token, setToken] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleRequest() {
    if (!email.trim()) {
      Alert.alert('Error', 'Por favor ingresa tu correo electrónico');
      return;
    }
    setLoading(true);
    try {
      const { data } = await authService.requestPasswordReset(email.trim());
      if (data.reset_token) {
        setToken(data.reset_token);
        Alert.alert(
          'Código generado',
          'Tu código de recuperación ya se escribió en el siguiente paso. Define tu nueva contraseña.'
        );
      } else {
        Alert.alert(
          'Revisa tu correo',
          'Si existe una cuenta asociada, recibirás un código. Pégalo en el siguiente paso.'
        );
      }
      setStep(2);
    } catch (e) {
      Alert.alert('Error', apiMessage(e, 'No se pudo solicitar la recuperación'));
    } finally {
      setLoading(false);
    }
  }

  async function handleConfirm() {
    if (!token.trim() || !newPassword || !confirmPassword) {
      Alert.alert('Error', 'Completa todos los campos');
      return;
    }
    if (newPassword !== confirmPassword) {
      Alert.alert('Error', 'Las contraseñas no coinciden');
      return;
    }
    if (newPassword.length < 8) {
      Alert.alert('Error', 'La contraseña debe tener al menos 8 caracteres');
      return;
    }
    setLoading(true);
    try {
      await authService.confirmPasswordReset(token.trim(), newPassword);
      Alert.alert('Contraseña actualizada', 'Ya puedes iniciar sesión con tu nueva contraseña.', [
        { text: 'OK', onPress: () => navigation.goBack() },
      ]);
    } catch (e) {
      Alert.alert('Error', apiMessage(e, 'No se pudo restablecer la contraseña'));
    } finally {
      setLoading(false);
    }
  }

  function field(label, icon, props) {
    return (
      <View style={styles.inputContainer}>
        <Text style={styles.label}>{label}</Text>
        <View style={styles.inputWrapper}>
          <MaterialCommunityIcons name={icon} size={20} color="#999" style={styles.inputIcon} />
          <TextInput
            style={styles.input}
            placeholderTextColor="#999"
            autoCapitalize="none"
            autoCorrect={false}
            {...props}
          />
        </View>
      </View>
    );
  }

  return (
    <KeyboardAvoidingView
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
      style={styles.container}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <TouchableOpacity style={styles.backBtn} onPress={() => navigation.goBack()}>
          <MaterialCommunityIcons name="arrow-left" size={24} color="#34A853" />
        </TouchableOpacity>

        <View style={styles.header}>
          <Text style={styles.title}>Recuperar Contraseña</Text>
          <Text style={styles.subtitle}>
            {step === 1
              ? 'Ingresa tu correo para recibir un código de recuperación.'
              : 'Escribe el código y tu nueva contraseña.'}
          </Text>
        </View>

        <View style={styles.form}>
          {step === 1 ? (
            <>
              {field('CORREO ELECTRÓNICO', 'email-outline', {
                placeholder: 'usuario@udec.edu.co',
                value: email,
                onChangeText: setEmail,
                keyboardType: 'email-address',
              })}
              <TouchableOpacity
                style={[styles.button, loading && styles.buttonDisabled]}
                onPress={handleRequest}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <View style={styles.buttonRow}>
                    <Text style={styles.buttonText}>Enviar código</Text>
                    <MaterialCommunityIcons name="send" size={20} color="#fff" />
                  </View>
                )}
              </TouchableOpacity>
            </>
          ) : (
            <>
              {field('CÓDIGO DE RECUPERACIÓN', 'key-outline', {
                placeholder: 'Código',
                value: token,
                onChangeText: setToken,
              })}
              {field('NUEVA CONTRASEÑA', 'lock-outline', {
                placeholder: 'Mínimo 8 caracteres',
                value: newPassword,
                onChangeText: setNewPassword,
                secureTextEntry: true,
              })}
              {field('CONFIRMAR CONTRASEÑA', 'lock-check-outline', {
                placeholder: 'Repite la contraseña',
                value: confirmPassword,
                onChangeText: setConfirmPassword,
                secureTextEntry: true,
              })}
              <TouchableOpacity
                style={[styles.button, loading && styles.buttonDisabled]}
                onPress={handleConfirm}
                disabled={loading}
              >
                {loading ? (
                  <ActivityIndicator color="#fff" />
                ) : (
                  <View style={styles.buttonRow}>
                    <Text style={styles.buttonText}>Cambiar contraseña</Text>
                    <MaterialCommunityIcons name="check" size={20} color="#fff" />
                  </View>
                )}
              </TouchableOpacity>
            </>
          )}

          <TouchableOpacity style={styles.backButton} onPress={() => navigation.goBack()}>
            <View style={styles.dashedBorder}>
              <Text style={styles.backText}>Volver al inicio de sesión</Text>
            </View>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  scrollContent: {
    flexGrow: 1,
    padding: 24,
    paddingTop: 48,
  },
  backBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 48,
  },
  header: {
    marginBottom: 48,
  },
  title: {
    fontSize: 26,
    fontWeight: 'bold',
    color: '#34A853',
    textAlign: 'center',
  },
  subtitle: {
    fontSize: 14,
    color: '#666',
    marginTop: 8,
    textAlign: 'center',
    paddingHorizontal: 40,
  },
  form: {
    width: '100%',
  },
  inputContainer: {
    marginBottom: 24,
  },
  label: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#666',
    marginBottom: 8,
    letterSpacing: 1,
  },
  inputWrapper: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
    borderRadius: 30,
    paddingHorizontal: 20,
    height: 56,
  },
  inputIcon: {
    marginRight: 12,
  },
  input: {
    flex: 1,
    fontSize: 16,
    color: '#333',
  },
  button: {
    backgroundColor: '#34A853',
    borderRadius: 30,
    height: 56,
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
    shadowColor: '#34A853',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 8,
    elevation: 4,
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  buttonRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontSize: 16,
    fontWeight: 'bold',
    marginRight: 8,
  },
  backButton: {
    marginTop: 48,
    alignItems: 'center',
  },
  dashedBorder: {
    borderWidth: 1,
    borderColor: '#34A853',
    borderStyle: 'dashed',
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 4,
  },
  backText: {
    color: '#34A853',
    fontSize: 14,
    fontWeight: '600',
  },
});
