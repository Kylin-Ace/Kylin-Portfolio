document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle functionality
    const themeToggle = document.getElementById('themeToggle');
    const sunIcon = document.getElementById('sunIcon');
    const moonIcon = document.getElementById('moonIcon');
    const html = document.documentElement;

    // Check for saved theme preference, otherwise use system preference
    const savedTheme = localStorage.getItem('theme');
    const systemDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && systemDarkMode)) {
        html.classList.add('dark');
        sunIcon.classList.remove('hidden');
        moonIcon.classList.add('hidden');
    } else {
        html.classList.remove('dark');
        sunIcon.classList.add('hidden');
        moonIcon.classList.remove('hidden');
    }

    // Theme toggle handler
    themeToggle.addEventListener('click', () => {
        html.classList.toggle('dark');
        sunIcon.classList.toggle('hidden');
        moonIcon.classList.toggle('hidden');
        
        // Save preference to localStorage
        const isDark = html.classList.contains('dark');
        localStorage.setItem('theme', isDark ? 'dark' : 'light');

        // Add animation to icons
        const activeIcon = isDark ? sunIcon : moonIcon;
        activeIcon.classList.add('transform', 'rotate-0');
        activeIcon.animate([
            { transform: 'rotate(-180deg)' },
            { transform: 'rotate(0)' }
        ], {
            duration: 300,
            easing: 'ease-out'
        });
    });

    // Handle system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                html.classList.add('dark');
                sunIcon.classList.remove('hidden');
                moonIcon.classList.add('hidden');
            } else {
                html.classList.remove('dark');
                sunIcon.classList.add('hidden');
                moonIcon.classList.remove('hidden');
            }
        }
    });

    // Mobile menu functionality
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            const isExpanded = mobileMenuBtn.getAttribute('aria-expanded') === 'true';
            
            mobileMenu.classList.toggle('hidden');
            mobileMenuBtn.setAttribute('aria-expanded', !isExpanded);

            // Animate mobile menu
            if (!mobileMenu.classList.contains('hidden')) {
                mobileMenu.animate([
                    { opacity: 0, transform: 'translateY(-1rem)' },
                    { opacity: 1, transform: 'translateY(0)' }
                ], {
                    duration: 200,
                    easing: 'ease-out'
                });
            }
        });
    }
});