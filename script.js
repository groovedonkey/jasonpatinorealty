document.addEventListener('DOMContentLoaded', () => {
    // Header scroll effect
    window.addEventListener('scroll', function() {
        const header = document.getElementById('main-header');
        if (window.scrollY > 10) {
            header.classList.add('header-scroll');
        } else {
            header.classList.remove('header-scroll');
        }
    });

    // Slideshow logic
    function initializeSlideshow(id) {
        const slideshow = document.getElementById(id);
        if (!slideshow) return; // Exit if slideshow doesn't exist
        const wrapper = slideshow.querySelector('.slides-wrapper');
        const slides = slideshow.querySelectorAll('.slide');
        const prevButton = slideshow.querySelector('.prev');
        const nextButton = slideshow.querySelector('.next');
        const totalSlides = slides.length;
        let currentIndex = 0;

        function updateSlides() {
            if (wrapper) {
                wrapper.style.transform = `translateX(-${currentIndex * 100}%)`;
            }
            if (prevButton) {
                prevButton.style.display = currentIndex === 0 ? 'none' : 'flex';
            }
            if (nextButton) {
                nextButton.style.display = currentIndex === totalSlides - 1 ? 'none' : 'flex';
            }
        }

        if (prevButton) {
            prevButton.addEventListener('click', () => {
                if (currentIndex > 0) {
                    currentIndex--;
                    updateSlides();
                }
            });
        }

        if (nextButton) {
            nextButton.addEventListener('click', () => {
                if (currentIndex < totalSlides - 1) {
                    currentIndex++;
                    updateSlides();
                }
            });
        }

        updateSlides();
    }

    // Initialize all slideshows
    initializeSlideshow('slideshow1');
    initializeSlideshow('slideshow2');
    initializeSlideshow('slideshow3');
    initializeSlideshow('slideshow-real-estate');
    initializeSlideshow('slideshow-team');

    // Smooth scrolling for ALL navigation links (desktop and mobile)
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Hamburger Menu Logic
    const hamburgerButton = document.getElementById('hamburger-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (hamburgerButton && mobileMenu) {
        // Toggle menu on hamburger click
        hamburgerButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });

        // Close menu when a link inside it is clicked
        const mobileMenuLinks = mobileMenu.querySelectorAll('a');
        mobileMenuLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.add('hidden');
            });
        });
    }
});