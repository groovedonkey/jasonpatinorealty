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

    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
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
});