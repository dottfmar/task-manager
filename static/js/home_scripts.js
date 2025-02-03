function revealPage() {
  document.getElementById('splash-overlay').style.opacity = '0';
  setTimeout(() => {
    document.getElementById('splash-overlay').style.display = 'none';
    document.getElementById('main-content').style.display = 'flex';
  }, 500);
}