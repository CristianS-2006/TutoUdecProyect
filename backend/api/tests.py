from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Materia, Tutor, Tutoria

class MateriaAPITestCase(APITestCase):
    def setUp(self):
        self.materia_data = {'nombre': 'Matemáticas', 'descripcion': 'Curso de matemáticas básicas'}
        self.url = reverse('materia-list')

    def test_create_materia(self):
        admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='pass12345'
        )
        self.client.force_authenticate(user=admin)
        response = self.client.post(self.url, self.materia_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Materia.objects.count(), 1)
        self.assertEqual(Materia.objects.get().nombre, 'Matemáticas')

    def test_anonymous_cannot_create_materia(self):
        response = self.client.post(self.url, self.materia_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_materias(self):
        Materia.objects.create(**self.materia_data)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

class TutorAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tutor1', password='pass123')
        self.materia = Materia.objects.create(nombre='Física')
        self.tutor_data = {
            'usuario_id': self.user.id,
            'especialidad': 'Física Cuántica',
            'materias_ids': [self.materia.id],
            'nivel_experiencia': 'experto',
            'tarifa_por_hora': 50.00
        }
        self.url = reverse('tutor-list')

    def test_create_tutor(self):
        admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='pass12345'
        )
        self.client.force_authenticate(user=admin)
        response = self.client.post(self.url, self.tutor_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tutor.objects.count(), 1)

    def test_get_tutores(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DashboardAPITestCase(APITestCase):
    def setUp(self):
        self.url = reverse('dashboard-resumen')
        self.admin = User.objects.create_superuser(
            username='admin', email='admin@example.com', password='pass12345'
        )
        self.student = User.objects.create_user(
            username='estudiante', password='pass12345'
        )
        self.tutor_user = User.objects.create_user(
            username='tutor', password='pass12345'
        )
        self.materia = Materia.objects.create(nombre='Matemáticas')
        self.tutor = Tutor.objects.create(
            usuario=self.tutor_user, especialidad='Matemáticas'
        )
        Tutoria.objects.create(
            tutor=self.tutor,
            estudiante=self.student,
            materia=self.materia,
            fecha_inicio=timezone.now(),
            duracion_minutos=60,
            estado='completada',
        )

    def test_summary_returns_aggregates_only_to_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['indicadores']['tutorias'], 1)
        completed = next(
            item
            for item in response.data['tutorias_por_estado']
            if item['estado'] == 'completada'
        )
        self.assertEqual(completed['total'], 1)
        self.assertEqual(len(response.data['tutorias_por_mes']), 6)
        self.assertEqual(
            response.data['tutorias_por_materia'][0],
            {'nombre': 'Matemáticas', 'total': 1},
        )
        self.assertNotIn('estudiante', response.data)

    def test_summary_is_forbidden_for_regular_users(self):
        self.client.force_authenticate(user=self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ChatbotAPITestCase(APITestCase):
    url = '/api/chatbot/chat/'

    def ask(self, message, **extra):
        return self.client.post(self.url, {'message': message, **extra}, format='json')

    def test_rejects_empty_message(self):
        self.assertEqual(self.ask('   ').status_code, status.HTTP_400_BAD_REQUEST)

    def test_university_questions(self):
        cases = {
            'que es la udec': 'universidad',
            'como me inscribo en la universidad': 'admision_universidad',
            'hay gratuidad': 'gratuidad',
            'quien es el rector': 'directivos',
        }
        for message, intent in cases.items():
            self.assertEqual(self.ask(message).data['intent'], intent, message)

    def test_unknown_question_admits_ignorance(self):
        data = self.ask('cual es el clima en marte').data
        self.assertEqual(data['intent'], 'default')
        self.assertIn('No tengo informaci', data['bot_response'])
        self.assertTrue(data['suggestions'])

    def test_returns_enterprise_5_json_payload(self):
        data = self.ask('que es la udec').data
        self.assertEqual(data['response_json']['standard'], 'empresarial-5.0')
        self.assertIn(data['response_json']['mode'], ('rules', 'ai'))
        self.assertIn('business_5_0', data['response_json'])
        self.assertIn('answer', data['response_json'])
        self.assertEqual(data['bot_response'], data['response_json']['answer'])

class AuthFlowAPITestCase(APITestCase):
    def test_register_tutor_and_student(self):
        for role in ('estudiante', 'tutor'):
            resp = self.client.post('/api/auth/register/', {
                'username': f'u_{role}', 'email': f'{role}@udec.edu.co', 'password': 'Prueba123',
                'first_name': 'Ana', 'last_name': 'Perez', 'role': role, 'especialidad': 'Matematicas',
            }, format='json')
            self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Tutor.objects.filter(usuario__username='u_tutor').exists())

    def test_password_reset_flow(self):
        User.objects.create_user('ana', 'ana@udec.edu.co', 'Vieja1234')
        with self.settings(PASSWORD_RESET_SHOW_TOKEN=True):
            resp = self.client.post('/api/auth/request_password_reset/', {'identifier': 'ana@udec.edu.co'}, format='json')
        self.assertEqual(resp.status_code, 200)
        token = resp.data['reset_token']
        resp = self.client.post('/api/auth/confirm_password_reset/', {'token': token, 'new_password': 'Nueva1234'}, format='json')
        self.assertEqual(resp.status_code, 200)
        login = self.client.post('/api/auth/login/', {'username': 'ana', 'password': 'Nueva1234'}, format='json')
        self.assertEqual(login.status_code, 200)

    def test_reset_token_hidden_by_default(self):
        User.objects.create_user('bea', 'bea@udec.edu.co', 'Vieja1234')
        resp = self.client.post('/api/auth/request_password_reset/', {'identifier': 'bea@udec.edu.co'}, format='json')
        self.assertNotIn('reset_token', resp.data)
