from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from users.models import Profile, PermissionAtom, UserProfileAssignment, PermissionAuditLog
from users.permissions import has_custom_permission

class AuthTestCase(APITestCase):

    def setUp(self):
        # Crear perfiles requeridos para el test
        self.base_profile = Profile.objects.create(
            name="Comprar en la tienda",
            description="Perfil base"
        )
        self.premium_profile = Profile.objects.create(
            name="Tutor Visual IA",
            description="Perfil premium"
        )
        
        # Crear permiso atómico
        self.perm_tutor = PermissionAtom.objects.create(
            code="tutor.acceder",
            module="tutor",
            description="Acceso tutor"
        )

    def test_user_registration_assigns_base_profile(self):
        """
        RN_LOGIN_01: Todo usuario registrado recibe automáticamente el perfil 'Comprar en la tienda'.
        """
        url = reverse('auth-register')
        data = {
            "username": "nuevo_comprador",
            "email": "nuevo.comprador@tienda.com",
            "password": "ClaveSegura123*",
            "first_name": "Nuevo",
            "last_name": "Comprador"
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que el usuario exista
        user = User.objects.get(username="nuevo_comprador")
        self.assertIsNotNone(user)
        
        # Verificar que tenga asignado el perfil base
        assignments = UserProfileAssignment.objects.filter(user=user, profile=self.base_profile)
        self.assertTrue(assignments.exists())
        self.assertTrue(assignments.first().is_active)
        
        # Verificar que se registró en la auditoría
        audit_log = PermissionAuditLog.objects.filter(user=user, profile=self.base_profile, action='assign')
        self.assertTrue(audit_log.exists())

    def test_login_traditional_returns_jwt_tokens(self):
        """
        El login tradicional retorna tokens de acceso y refresco JWT válidos.
        """
        user = User.objects.create_user(
            username="tester",
            email="tester@tienda.com",
            password="ClaveSegura123*"
        )
        
        url = reverse('auth-login')
        data = {
            "username": "tester",
            "password": "ClaveSegura123*"
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_password_recovery_flow(self):
        """
        Prueba el flujo completo de solicitar recuperación y cambiar contraseña con token.
        """
        # 1. Crear usuario con contraseña
        user = User.objects.create_user(
            username="recuperador",
            email="recuperador@tienda.com",
            password="ClaveOriginal123*"
        )
        
        # 2. Solicitar enlace de recuperación
        reset_request_url = reverse('password-reset-request')
        response = self.client.post(reset_request_url, {"email": "recuperador@tienda.com"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 3. Simular generación de token y uid (lo que hace la vista)
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        # 4. Confirmar restablecimiento de contraseña
        reset_confirm_url = reverse('password-reset-confirm')
        data_confirm = {
            "token": token,
            "uid": uidb64,
            "new_password": "NuevaClaveSuperSegura456!"
        }
        response_confirm = self.client.post(reset_confirm_url, data_confirm, format='json')
        self.assertEqual(response_confirm.status_code, status.HTTP_200_OK)
        
        # 5. Intentar login con la nueva contraseña
        login_url = reverse('auth-login')
        data_login = {
            "username": "recuperador",
            "password": "NuevaClaveSuperSegura456!"
        }
        response_login = self.client.post(login_url, data_login, format='json')
        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_login.data)
