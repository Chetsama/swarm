// Theme toggle functionality
const themeToggle = document.getElementById('theme-toggle');
const savedTheme = localStorage.getItem('theme');

// Initialize theme if not set
if (!savedTheme) {
  localStorage.setItem('theme', 'dark');
  document.body.setAttribute('data-theme', 'dark');
} else {
  document.body.setAttribute('data-theme', savedTheme);
}

themeToggle.addEventListener('click', () => {
  const currentTheme = document.body.getAttribute('data-theme');
  const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

  document.body.setAttribute('data-theme', newTheme);
  localStorage.setItem('theme', newTheme);
});