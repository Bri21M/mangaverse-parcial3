// MangaVerse — main.js

function toggleMenu() {
  document.querySelector('.nav-links').classList.toggle('open');
}

// Auto-hide flash messages
document.addEventListener('DOMContentLoaded', () => {
  const flashes = document.querySelectorAll('.flash');
  flashes.forEach(f => {
    setTimeout(() => {
      f.style.transition = 'opacity 0.5s';
      f.style.opacity = '0';
      setTimeout(() => f.remove(), 500);
    }, 3500);
  });

  // Animate cards on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.style.opacity = '1';
        e.target.style.transform = 'translateY(0)';
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.manga-card, .featured-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
});

// Favourite toggle
async function toggleFav(mangaId, btn) {
  try {
    const res = await fetch(`/favorito/${mangaId}`, { method: 'POST' });
    const data = await res.json();
    if (data.estado === 'agregado') {
      btn.textContent = '❤ En favoritos';
      btn.classList.add('fav-active');
    } else {
      btn.textContent = '♡ Añadir a favoritos';
      btn.classList.remove('fav-active');
    }
  } catch (e) {
    console.error('Error toggling favourite:', e);
  }
}
