<template>
    <div class="layout-container">
        <!-- Navbar -->
        <header class="navbar">
            <div class="navbar-container">
                <router-link to="/" class="navbar-logo">
                    <span class="brand-text">TutoUdec</span>
                </router-link>

                <!-- Botón mobile -->
                <button class="navbar-toggler" @click="mobileMenuOpen = !mobileMenuOpen">
                    <span class="navbar-toggler-icon">☰</span>
                </button>

                <div :class="['navbar-collapse', { open: mobileMenuOpen }]">
                    <nav>
                        <ul class="navbar-menu">
                            <li>
                                <router-link to="/">Inicio</router-link>
                            </li>
                            <li>
                                <router-link to="/tutores">Tutores</router-link>
                            </li>
                            <li>
                                <router-link to="/materias">Materias</router-link>
                            </li>
                            <li>
                                <router-link to="/chatbot">Chatbot</router-link>
                            </li>
                            <li v-if="auth.isAuthenticated">
                                <router-link to="/tutorias">Mis tutorías</router-link>
                            </li>
                            <li v-if="auth.user?.role === 'admin'">
                                <router-link to="/dashboard">Dashboard</router-link>
                            </li>

                            <li v-if="!auth.isAuthenticated">
                                <router-link to="/sesion" class="cta-button">
                                    Iniciar sesión
                                </router-link>
                            </li>
                            <li v-if="!auth.isAuthenticated">
                                <router-link to="/formulario">Registro</router-link>
                            </li>
                            <li v-else class="user-row">
                                <span class="user-name">{{ greeting }}</span>
                                <button type="button" class="logout-btn" @click="logout">
                                    Salir
                                </button>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </header>

        <main>
            <router-view />
        </main>

        <!-- Footer -->
        <footer class="footer">
            <div class="footer-container">
                <div class="footer-column">
                    <p class="footer-description">
                        TutoUdec - Plataforma de tutorías entre estudiantes de la Universidad de Cundinamarca.
                    </p>
                </div>

                <div class="footer-column">
                    <h4>Links</h4>
                    <ul>
                        <li><router-link to="/">Inicio</router-link></li>
                    </ul>
                </div>

                <div class="footer-column">
                    <h4>Contact</h4>
                    <p><i class="fas fa-map-marker-alt"></i>Universidad de Cundinamarca - Seccional Girardot</p>
                    <p><i class="fas fa-phone"></i>300 000 0000 313 000 0000</p>
                    <p><i class="fas fa-envelope"></i>info@tutoudec.com</p>
                </div>
            </div>
            <div class="footer-bottom">
                Derechos Reservados 2024 TutoUdec
            </div>
        </footer>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const router = useRouter();
const auth = useAuthStore();

const mobileMenuOpen = ref(false);

const greeting = computed(() => {
    const u = auth.user;
    if (!u) return '';
    const name = [u.first_name, u.last_name].filter(Boolean).join(' ');
    return name || u.username || '';
});

function logout() {
    auth.logout();
    mobileMenuOpen.value = false;
    router.push('/');
}
</script>

<style>
:root {
    /* Colores del logo */
    --color-amarillo: #FFF52D;
    --color-verde: #34A853;
    --color-blanco: #FFFFFF;
    --color-negro-texto: #1E1E1E;
    --gris--bonito: #F3F6FA;
    /* gris sólido sin transparencia */
    --borde-gris: #B4B9BE;
    /* gris sólido */

    /* Colores adicionales elegantes */
    --color-fondo: #F9F9F9;
    --color-contraste: #3F4E65;
    --color-acento: #B8860B;

    /* Grises para navbar y elementos */
    --gris-suave: #A8A8A8;
    --gris-oscuro: #4B5563;
}

/* Navbar */
.navbar {
    background: var(--gris--bonito);
    border-bottom: 1px solid var(--borde-gris);
    position: sticky;
    padding: 1.25rem 0;
    top: 0;
    z-index: 999;
    font-weight: 500;
    color: var(--color-negro-texto);
    user-select: none;
}

.navbar-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 2rem;
}

.brand-text {
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--color-verde);
    text-decoration: none;
}

.navbar-logo img {
    height: 64px;
    object-fit: contain;
    transition: transform 0.3s ease;
    filter: drop-shadow(0 1px 1px rgba(75, 85, 99, 0.3));
    padding-right: 1rem;
}

.user-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.user-name {
    font-size: 0.95rem;
    color: var(--gris-oscuro);
    max-width: 160px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.logout-btn {
    background: transparent;
    border: 1.5px solid var(--borde-gris);
    border-radius: 10px;
    padding: 0.5rem 0.9rem;
    font-weight: 600;
    cursor: pointer;
    color: var(--color-negro-texto);
}

.logout-btn:hover {
    border-color: var(--gris-oscuro);
}

.navbar-logo:hover img {
    transform: scale(1.05);
}

/* Menú principal */
.navbar-menu {
    display: flex;
    list-style: none;
    gap: 2.5rem;
    align-items: center;
    margin: 0;
    padding: 0;
}

.navbar-menu li {
    position: relative;
}

/* Links normales y dropdown toggles */
.navbar-menu a:not(.cta-button),
.dropdown-toggle {
    font-size: 17px;
    font-weight: 500;
    color: var(--color-negro-texto);
    text-decoration: none;
    padding: 0.75rem 1.2rem;
    border-radius: 10px;
    transition: background-color 0.3s ease, color 0.3s ease;
    background: transparent;
    cursor: pointer;
    user-select: none;
    border: 1.5px solid transparent;
    box-shadow: inset 0 0 0 0 transparent;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.navbar-menu a:not(.cta-button):hover,
.dropdown-toggle:hover {
    background-color: var(--gris-suave);
    color: var(--color-negro-texto);
    border-color: var(--gris-oscuro);
    box-shadow: inset 0 0 8px rgba(0, 0, 0, 0.1);
}

/* Botón "Acceder" */
.cta-button {
    background-color: var(--color-verde);
    color: var(--color-blanco);
    border-radius: 25px;
    padding: 0.55rem 1.5rem;
    font-size: 16px;
    font-weight: 700;
    transition: background 0.3s ease, color 0.3s ease, box-shadow 0.3s ease;
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    text-decoration: none;
    user-select: none;
    border: 1.5px solid var(--gris-suave);
    box-shadow: 0 2px 6px rgba(75, 85, 99, 0.25);
}

.cta-button:hover {
    background-color: var(--gris-oscuro);
    color: var(--color-blanco);
    border-color: var(--gris-oscuro);
    box-shadow: 0 6px 12px rgba(75, 85, 99, 0.45);
}

/* Estilo para el badge contador totalPQRS */
.badge {
    background-color: var(--color-verde);
    /* o usa otro color que resalte */
    color: var(--color-blanco);
    font-size: 12px;
    font-weight: 700;
    padding: 3px 7px;
    border-radius: 9999px;
    /* círculo perfecto */
    min-width: 20px;
    height: 20px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    position: relative;
    top: -8px;
    left: -6px;
    box-shadow: 0 0 4px rgba(0, 0, 0, 0.2);
    user-select: none;
    pointer-events: none;
    transition: background-color 0.3s ease;
}

/* Variante para badge redondo más pequeño */
.badge.rounded-circle {
    border-radius: 50%;
}


/* Dropdown listado */
.dropdown-list {
    list-style: none;
    display: block;
    position: absolute;
    top: 110%;
    left: 0;
    background: var(--color-blanco);
    border: 1.8px solid var(--gris-suave);
    border-radius: 12px;
    min-width: 240px;
    box-shadow: 0 12px 24px rgba(75, 85, 99, 0.15);
    padding: 0.6rem 0;
    z-index: 1100;
    user-select: none;
    opacity: 0;
    pointer-events: none;
    transform: translateY(-10px) scale(0.98);
    transition: opacity 0.28s cubic-bezier(.4, 1.3, .5, 1), transform 0.28s cubic-bezier(.4, 1.3, .5, 1);
}

.dropdown-list.visible {
    display: block;
    opacity: 1;
    pointer-events: auto;
}

.dropdown-list li a {
    display: block;
    padding: 0.65rem 1.3rem;
    color: var(--gris-oscuro);
    font-size: 15px;
    transition: background-color 0.25s ease, color 0.25s ease;
    border-radius: 8px;
    font-weight: 500;
}

.dropdown-list li a:hover {
    background-color: var(--gris-suave);
    color: var(--gris-oscuro);
}

/* Submenú anidado (MenuRecursivo) */
.dropdown-list li ul {
    margin-left: 1.3rem;
    padding-left: 0.7rem;
    border-left: 2px solid var(--gris-suave);
}

.dropdown-list li ul li {
    margin-top: 0.3rem;
}

.dropdown-list li ul li a {
    padding: 0.45rem 1.3rem;
    font-size: 14px;
    color: var(--gris-oscuro);
    font-weight: 400;
}

/* Saludo */
.navbar-menu li h2 {
    margin: 0;
    font-weight: 600;
    font-size: 18px;
    color: var(--gris-oscuro);
    padding-left: 1rem;
    user-select: none;
}

/* Footer */
.footer {
    background-color: var(--gris--bonito);
    padding: 2.5rem 2rem;
    border-top: 1.5px solid var(--borde-gris);
    color: var(--color-negro-texto);
    user-select: none;
}

.footer-container {
    display: flex;
    justify-content: space-between;
    gap: 2.5rem;
    max-width: 1280px;
    margin: 0 auto;
    flex-wrap: wrap;
}

.footer-column {
    flex: 1 1 20%;
    min-width: 160px;
}

.footer-logo {
    max-width: 250px;
    margin-bottom: 1.3rem;
    filter: drop-shadow(0 1px 2px var(--borde-gris));
}

.footer-description {
    font-size: 15px;
    line-height: 1.7;
    color: var(--gris-suave);
    user-select: text;
}

.footer-column h4 {
    font-size: 17px;
    margin-bottom: 1rem;
    font-weight: 700;
    color: var(--color-negro-texto);
}

.footer-column ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.footer-column ul li {
    margin: 0.5rem 0;
}

.footer-column a {
    text-decoration: none;
    color: var(--color-negro-texto);
    font-size: 15px;
    transition: color 0.25s ease;
    user-select: text;
}

.footer-column a:hover {
    color: var(--color-acento);
    text-decoration: underline;
}

.footer-column i {
    margin-right: 8px;
    color: var(--color-verde);
}

.footer-bottom {
    text-align: center;
    padding-top: 1.8rem;
    font-size: 14px;
    color: var(--color-negro-texto);
    border-top: 1px solid var(--borde-gris);
    margin-top: 1.5rem;
}

/* Íconos sociales */
.social-icon {
    font-size: 1.3rem;
    color: var(--gris-oscuro);
    margin-right: 0.6rem;
    transition: color 0.3s ease;
}

.social-icon:hover {
    color: var(--color-acento);
}

/* Responsivo básico para navbar-menu */
@media (max-width: 900px) {
    .navbar-menu {
        gap: 1rem;
    }

    .navbar-menu li h2 {
        font-size: 16px;
    }
}

.layout-container {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
    /* altura minima*/
}

main {
    flex: 1;
    /* Crece para ocupar espacio disponible */
}

@media (max-width: 768px) {
    .navbar-menu {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .navbar-menu li {
        width: 100%;
        text-align: center;
    }

    .navbar-logo img {
        height: 50px;
        /* Ajusta el logo en pantallas pequeñas */
    }

    .footer-container {
        flex-direction: column;
        align-items: center;
    }

    .footer-column {
        text-align: center;
        margin-bottom: 1.5rem;
    }
}

.navbar-toggler {
    display: none;
    background: none;
    border: none;
    cursor: pointer;
    padding: 0.5rem 0.8rem;
    margin-left: auto;
}

.navbar-toggler-icon::before {
    top: -9px;
}

.navbar-toggler-icon::after {
    top: 9px;
}

/* Mostrar botón y ocultar menú horizontal en móvil */
@media (max-width: 768px) {
    .navbar-toggler {
        display: block;
    }

    .navbar-collapse {
        display: none;
        width: 100%;
    }

    .navbar-collapse.open {
        display: block;
        background: var(--gris--bonito);
        position: absolute;
        top: 100%;
        left: 0;
        box-shadow: 0 8px 24px rgba(75, 85, 99, 0.08);
        z-index: 1200;
        padding: 1.2rem 0 1.2rem 0;
        animation: fadeInMenu 0.25s;
    }

    .navbar-menu {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
    }

    .navbar-menu li {
        width: 100%;
        text-align: center;
    }

    .navbar-logo {
        z-index: 1300;
    }
}

/* Animación de aparición */
@keyframes fadeInMenu {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>