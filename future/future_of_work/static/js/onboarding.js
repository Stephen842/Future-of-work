// Select steps and progress UI
const steps = [
  document.getElementById("step-1"),
  document.getElementById("step-2"),
  document.getElementById("step-3")
];
const progressBar = document.getElementById("progress-bar");
const progressLabel = document.getElementById("progress-label");

let currentStep = 0;
let selectedPod = "";
let selectedGoal = "";

// Step Navigation
function moveToStep(stepIdx) {
  steps.forEach((s, i) => s.classList.toggle("hidden", i !== stepIdx));
  
  currentStep = stepIdx;

  if (progressBar) {
    progressBar.style.width = `${((stepIdx + 1) / steps.length) * 100}%`;
  }
  if (progressLabel) {
    progressLabel.textContent = `Step ${stepIdx + 1} of 3`;
  }

  if (stepIdx === 0) nextToStep2.disabled = !selectedPod;
  if (stepIdx === 1) nextToStep3.disabled = !selectedGoal;
}

// Step 1: Pod Selection
const podCards = document.querySelectorAll(".pod-card");
const nextToStep2 = document.getElementById("next-to-step-2");

podCards.forEach(card => {
  card.addEventListener("click", function () {
    podCards.forEach(c => c.classList.remove("border-gold", "ring-2"));
    this.classList.add("border-gold", "ring-2");
    selectedPod = this.getAttribute("data-pod");
    nextToStep2.disabled = false;
  });
});

nextToStep2.addEventListener("click", () => moveToStep(1));

// Step 2: Goal Selection
const backToStep1 = document.getElementById("back-to-step-1");
const nextToStep3 = document.getElementById("next-to-step-3");
const goalRadios = document.querySelectorAll("input[name='goal']");

goalRadios.forEach(radio => {
  radio.addEventListener("change", function () {
    selectedGoal = this.value;
    nextToStep3.disabled = false;
  });
});

backToStep1.addEventListener("click", () => moveToStep(0));
nextToStep3.addEventListener("click", () => moveToStep(2));

// Step 3: Form & Validation
const onboardingForm = document.getElementById("onboarding-form");
const backToStep2 = document.getElementById("back-to-step-2");
const pwErr = document.getElementById("onboarding-pw-error");

backToStep2.addEventListener("click", () => moveToStep(1));

onboardingForm.addEventListener("submit", function (e) {
  const pw1 = document.getElementById('onboarding-password').value;
  const pw2 = document.getElementById('onboarding-password-confirm').value;

  pwErr.classList.add('hidden');

  // Basic front-end password validation (Django handles the rest)
  if (pw1.length < 8) {
    e.preventDefault();
    pwErr.textContent = 'Password must be at least 8 characters.';
    pwErr.classList.remove('hidden');
    return;
  }

  if (pw1 !== pw2) {
    e.preventDefault();
    pwErr.textContent = 'Passwords do not match.';
    pwErr.classList.remove('hidden');
    return;
  }

  // Pass Pod & Goal into the form POST fields
  document.getElementById("selected-pod").value = selectedPod;
  document.getElementById("selected-goal").value = selectedGoal;

  // Submit continues to Django — normal behavior
});

// Initialize first step
moveToStep(0);
