// DataForge — Main JS
document.addEventListener('DOMContentLoaded', () => {
  // Mobile nav toggle
  const toggle = document.getElementById('nav-toggle');
  const links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', () => links.classList.toggle('open'));
  }

  // Auto-dismiss alerts after 5s
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => alert.remove(), 5000);
  });
});
