// Auth page logic (Django authentication only)

const regBtn = document.getElementById('auth-register-btn');
const loginBtn = document.getElementById('auth-login-btn');
const loginForm = document.getElementById('user-login-form');
const forgotPwLink = document.getElementById('forgot-password-link');
const resetPwForm = document.getElementById('reset-password-form');

// Redirect to registration
regBtn && (regBtn.onclick = () => {
    window.location = onboardingUrl;
});

// Show login form & hide reset form
loginBtn && (loginBtn.onclick = () => {
    loginForm.classList.remove('hidden');
    resetPwForm && resetPwForm.classList.add('hidden');
});

// Forgot password: show reset form
forgotPwLink && (forgotPwLink.onclick = (e) => {
    e.preventDefault();
    loginForm.classList.add('hidden');
    resetPwForm.classList.remove('hidden');
});

// Automatically show login form if backend sends validation errors
document.addEventListener('DOMContentLoaded', () => {
    const hasError = document.querySelector('.messages li.error');
    if (hasError && loginForm) {
        loginForm.classList.remove('hidden');
    }
});