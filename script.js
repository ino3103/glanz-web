// ===================================
// GLANZ Wellness Hub - JavaScript
// ===================================

// ===================================
// LANGUAGE SWITCHING
// ===================================
let currentLang = localStorage.getItem('glanz_language') || 'en';

// Function to change language
function changeLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('glanz_language', lang);
    updateContent();
    updateLangButton();
}

// Function to update all translatable content
function updateContent() {
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[currentLang] && translations[currentLang][key]) {
            element.textContent = translations[currentLang][key];
        }
    });

    // Update placeholders
    const placeholders = document.querySelectorAll('[data-i18n-placeholder]');
    placeholders.forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        if (translations[currentLang] && translations[currentLang][key]) {
            element.placeholder = translations[currentLang][key];
        }
    });
}

// Function to update language button
function updateLangButton() {
    const langButton = document.getElementById('current-lang');
    if (langButton) {
        langButton.textContent = currentLang.toUpperCase();
    }
}

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {

    // Initialize language
    updateContent();
    updateLangButton();

    // Language switcher event listener
    const langSwitcher = document.getElementById('lang-switcher');
    if (langSwitcher) {
        langSwitcher.addEventListener('click', function () {
            const newLang = currentLang === 'en' ? 'sw' : 'en';
            changeLanguage(newLang);
        });
    }

    // ===================================
    // NAVIGATION
    // ===================================
    const navbar = document.getElementById('navbar');
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Navbar scroll effect
    window.addEventListener('scroll', function () {
        if (window.scrollY > 100) {
            navbar.style.padding = '0.75rem 0';
            navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.3)';
        } else {
            navbar.style.padding = '1.25rem 0';
            navbar.style.boxShadow = 'none';
        }
    });

    // Mobile menu toggle
    navToggle.addEventListener('click', function () {
        navMenu.classList.toggle('active');

        // Animate hamburger icon
        const spans = navToggle.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });

    // Close mobile menu when clicking on a link
    navLinks.forEach(link => {
        link.addEventListener('click', function () {
            navMenu.classList.remove('active');
            const spans = navToggle.querySelectorAll('span');
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        });
    });

    // ===================================
    // SMOOTH SCROLLING
    // ===================================
    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);

            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });

    // ===================================
    // SCROLL ANIMATIONS
    // ===================================
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe elements for scroll animations
    const animateElements = document.querySelectorAll(
        '.product-card, .benefit-card, .bundle-card, .testimonial-card, .gallery-item'
    );

    animateElements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(30px)';
        element.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(element);
    });

    // ===================================
    // FORM HANDLING
    // ===================================
    const contactForm = document.querySelector('.contact-form');

    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            const submitBtn = contactForm.querySelector('button[type="submit"]');
            const originalBtnText = submitBtn.textContent;

            // Show loading state
            submitBtn.textContent = translations[currentLang].form_sending || 'Sending...';
            submitBtn.disabled = true;

            // Get form data
            const formData = new FormData(contactForm);

            // Honeypot check
            if (formData.get('_gotcha')) {
                console.warn('Bot detected via honeypot');
                contactForm.reset();
                submitBtn.textContent = originalBtnText;
                submitBtn.disabled = false;
                return;
            }

            // Add configuration for FormSubmit.co
            formData.append('_captcha', 'false'); // Recommended to be false for AJAX to avoid redirects
            formData.append('_template', 'table'); // Use table template
            formData.append('_subject', `GLANZ Contact Form: ${formData.get('subject') || 'New Message'}`);

            // Send to FormSubmit.co
            fetch('https://formsubmit.co/ajax/inomosjac@gmail.com', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    // Show success message
                    alert(translations[currentLang].form_success || 'Thank you! Your message has been sent successfully.');

                    // Reset form
                    contactForm.reset();
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(translations[currentLang].form_error || 'Oops! Something went wrong. Please try again.');
                })
                .finally(() => {
                    // Restore button state
                    submitBtn.textContent = originalBtnText;
                    submitBtn.disabled = false;
                });
        });
    }

    // ===================================
    // ACTIVE NAVIGATION LINK
    // ===================================
    window.addEventListener('scroll', function () {
        let current = '';
        const sections = document.querySelectorAll('section[id]');

        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;

            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // ===================================
    // PARALLAX EFFECT FOR HERO
    // ===================================
    const heroImage = document.querySelector('.hero-image');

    if (heroImage) {
        window.addEventListener('scroll', function () {
            // Disable parallax on mobile/tablet for better performance and visibility
            if (window.innerWidth < 1024) {
                heroImage.style.transform = 'translateY(0)';
                return;
            }

            const scrolled = window.pageYOffset;
            const rate = scrolled * 0.2; // Reduced from 0.3 for subtler effect

            if (scrolled <= window.innerHeight) {
                // Limit the maximum translation to 100px to avoid hitting the trust badges
                const limitedRate = Math.min(rate, 100);
                heroImage.style.transform = `translateY(${limitedRate}px)`;
            }
        });
    }

    // ===================================
    // PRODUCT CARD TILT EFFECT
    // ===================================
    const productCards = document.querySelectorAll('.product-card');

    productCards.forEach(card => {
        card.addEventListener('mousemove', function (e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        });

        card.addEventListener('mouseleave', function () {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
        });
    });

    // ===================================
    // BEFORE/AFTER SLIDER INTERACTION
    // ===================================
    const sliderContainer = document.querySelector('.image-comparison');
    const afterImage = document.querySelector('.image-wrapper.after');
    const handle = document.querySelector('.handle');

    if (sliderContainer && afterImage && handle) {
        let isDragging = false;

        const moveSlider = (x) => {
            const rect = sliderContainer.getBoundingClientRect();
            let percentage = ((x - rect.left) / rect.width) * 100;

            // Clamp percentage between 0 and 100
            percentage = Math.max(0, Math.min(100, percentage));

            // Update mask and handle position
            afterImage.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
            handle.style.left = `${percentage}%`;
        };

        // Mouse Events
        sliderContainer.addEventListener('mousedown', () => isDragging = true);
        window.addEventListener('mouseup', () => isDragging = false);
        window.addEventListener('mousemove', (e) => {
            if (!isDragging) return;
            moveSlider(e.clientX);
        });

        // Touch Events
        sliderContainer.addEventListener('touchstart', () => isDragging = true);
        window.addEventListener('touchend', () => isDragging = false);
        window.addEventListener('touchmove', (e) => {
            if (!isDragging) return;
            moveSlider(e.touches[0].clientX);
        });

        // Handle click to jump
        sliderContainer.addEventListener('click', (e) => {
            moveSlider(e.clientX);
        });
    }

    // ===================================
    // FAQ ACCORDION
    // ===================================
    const faqItems = document.querySelectorAll('.faq-item');

    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');

        question.addEventListener('click', () => {
            const isActive = item.classList.contains('active');

            // Close all other items
            faqItems.forEach(faq => {
                faq.classList.remove('active');
            });

            // Toggle current item
            if (!isActive) {
                item.classList.add('active');
            }
        });
    });

    // ===================================
    // LOADING ANIMATION
    // ===================================
    window.addEventListener('load', function () {
        document.body.style.opacity = '0';
        setTimeout(function () {
            document.body.style.transition = 'opacity 0.5s ease';
            document.body.style.opacity = '1';
        }, 100);
    });

    // ===================================
    // COUNTER ANIMATION FOR STATS
    // ===================================
    const stats = document.querySelectorAll('.stat-number');
    let hasAnimated = false;

    const animateCounter = (element, target, duration) => {
        let start = 0;
        const increment = target / (duration / 16);

        const timer = setInterval(() => {
            start += increment;
            if (start >= target) {
                element.textContent = target;
                clearInterval(timer);
            } else {
                element.textContent = Math.floor(start);
            }
        }, 16);
    };

    window.addEventListener('scroll', function () {
        const aboutSection = document.querySelector('.about');
        if (aboutSection && !hasAnimated) {
            const rect = aboutSection.getBoundingClientRect();
            if (rect.top < window.innerHeight && rect.bottom >= 0) {
                hasAnimated = true;
                stats.forEach(stat => {
                    const text = stat.textContent;
                    // This is a simple implementation - you can enhance it
                    stat.style.opacity = '1';
                });
            }
        }
    });
});
