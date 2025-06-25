console.log("JavaScript is working!");
document.addEventListener("DOMContentLoaded", () => {
    const themeToggle = document.getElementById('themeToggle');
    const body = document.body;

    // Get theme from localStorage or system preference
    const getStoredTheme = () => {
        const storedTheme = localStorage.getItem('theme');
        const systemDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        return storedTheme || (systemDark ? 'dark' : 'light');
    };

    // Apply the given theme
    const applyTheme = (theme) => {
        if (theme === 'dark') {
            body.classList.add('dark');
            themeToggle.textContent = '☀️';
        } else {
            body.classList.remove('dark');
            themeToggle.textContent = '🌙';
        }
    };

    // Initialize theme
    const initialTheme = getStoredTheme();
    applyTheme(initialTheme);
    console.log("Initial theme applied:", initialTheme);

    // Toggle theme on button click
    themeToggle.addEventListener('click', () => {
        const newTheme = body.classList.contains('dark') ? 'light' : 'dark';
        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
        console.log("Theme toggled to:", newTheme);
    });

    // Watch for system theme changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
        if (!localStorage.getItem('theme')) {
            const newTheme = e.matches ? 'dark' : 'light';
            applyTheme(newTheme);
            console.log("System theme changed, applied:", newTheme);
        }
    });
});