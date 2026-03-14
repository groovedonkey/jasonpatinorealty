/* ============================================
   Jason Patino Realty - Main JavaScript
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {

  /* ---- Mobile Menu Toggle ---- */
  const menuButton = document.getElementById('mobile-menu-button');
  const mobileMenu = document.getElementById('mobile-menu');
  const openIcon = document.getElementById('menu-open-icon');
  const closeIcon = document.getElementById('menu-close-icon');

  if (menuButton && mobileMenu) {
    menuButton.addEventListener('click', () => {
      const isHidden = mobileMenu.classList.toggle('hidden');
      openIcon.classList.toggle('hidden', !isHidden);
      closeIcon.classList.toggle('hidden', isHidden);
      menuButton.setAttribute('aria-expanded', String(!isHidden));
    });

    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.add('hidden');
        openIcon.classList.remove('hidden');
        closeIcon.classList.add('hidden');
        menuButton.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---- Carousel Setup ---- */
  function setupCarousel(rootId, dotsId) {
    const root = document.getElementById(rootId);
    if (!root) return;

    const track = root.querySelector('.carousel-track');
    const slides = Array.from(track.querySelectorAll('.carousel-slide'));
    const dotsContainer = document.getElementById(dotsId);

    let currentGroup = 0;
    let slidesPerView = window.innerWidth >= 768 ? 3 : 1;
    let autoRotate;

    const groupCount = () => Math.max(1, Math.ceil(slides.length / slidesPerView));

    function renderDots() {
      if (!dotsContainer) return;
      dotsContainer.innerHTML = '';
      const total = groupCount();
      for (let i = 0; i < total; i++) {
        const dot = document.createElement('button');
        dot.className = 'carousel-dot' + (i === 0 ? ' active' : '');
        dot.setAttribute('aria-label', `Go to slide group ${i + 1}`);
        dot.addEventListener('click', () => {
          goTo(i);
          pause();
          resumeLater();
        });
        dotsContainer.appendChild(dot);
      }
    }

    function updateDots() {
      if (!dotsContainer) return;
      const dots = dotsContainer.querySelectorAll('.carousel-dot');
      dots.forEach((d, i) => d.classList.toggle('active', i === currentGroup));
    }

    function goTo(groupIndex) {
      const total = groupCount();
      currentGroup = (groupIndex + total) % total;
      track.style.transform = `translateX(-${100 * currentGroup}%)`;
      updateDots();
    }

    function next() { goTo(currentGroup + 1); }
    function pause() { clearInterval(autoRotate); }
    function start() {
      pause();
      autoRotate = setInterval(next, 10000);
    }
    function resumeLater() { setTimeout(start, 15000); }

    track.querySelectorAll('.carousel-video').forEach(card => {
      card.addEventListener('click', () => {
        pause();
        resumeLater();
      });
    });

    window.addEventListener('resize', () => {
      const newSPV = window.innerWidth >= 768 ? 3 : 1;
      if (newSPV !== slidesPerView) {
        slidesPerView = newSPV;
        track.style.transition = 'none';
        renderDots();
        goTo(0);
        setTimeout(() => {
          track.style.transition = 'transform .5s ease-in-out';
        }, 50);
      }
    });

    renderDots();
    goTo(0);
    start();
  }

  setupCarousel('carousel-brokerage', 'dots-brokerage');
  setupCarousel('carousel-vets', 'dots-vets');

  /* ---- Scroll Animations ---- */
  const elements = document.querySelectorAll('.fade-in-up, .slide-in-left, .slide-in-right');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      entry.target.classList.toggle('animate', entry.isIntersecting);
    });
  }, { threshold: 0.1 });

  elements.forEach(el => observer.observe(el));

  /* ---- Contact Form Submission ---- */
  const contactForm = document.getElementById('contact-form');
  const confirmationPopup = document.getElementById('confirmation-popup');
  const popupContent = document.getElementById('popup-content');
  const closePopupButton = document.getElementById('close-popup-btn');

  function showPopup() {
    confirmationPopup.classList.add('visible');
    setTimeout(() => {
      popupContent.classList.add('show');
    }, 10);
  }

  function closePopup() {
    popupContent.classList.remove('show');
    setTimeout(() => {
      confirmationPopup.classList.remove('visible');
      contactForm.reset();
    }, 300);
  }

  if (contactForm && confirmationPopup && closePopupButton) {
    contactForm.addEventListener('submit', async (e) => {
      e.preventDefault();

      const formData = new FormData(contactForm);
      const data = Object.fromEntries(formData.entries());

      // If a backend API is configured, POST to it
      if (CONFIG.API_BASE_URL) {
        try {
          const res = await fetch(`${CONFIG.API_BASE_URL}${CONFIG.CONTACT_ENDPOINT}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
          });
          if (!res.ok) throw new Error('Network response was not ok');
        } catch (err) {
          console.error('Contact form submission failed:', err);
          // Still show the popup so the user isn't left hanging;
          // backend errors can be handled more gracefully later.
        }
      }

      showPopup();
    });

    closePopupButton.addEventListener('click', closePopup);
    confirmationPopup.addEventListener('click', (e) => {
      if (e.target === confirmationPopup) closePopup();
    });
  }
});
