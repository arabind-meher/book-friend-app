(function () {
    const STORAGE_KEY = 'theme';
    const root = document.documentElement;

    function applyTheme(theme) {
        if (theme === 'dark') root.classList.add('dark');
        else root.classList.remove('dark');
    }

    // Initialize from saved or system
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) applyTheme(saved);
    else if (window.matchMedia?.('(prefers-color-scheme: dark)').matches) applyTheme('dark');

    // Bind on ready
    window.addEventListener('DOMContentLoaded', () => {
        const buttons = [
            ...document.querySelectorAll('#themeToggle'),
            ...document.querySelectorAll('[data-theme-toggle]')
        ];
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const nowDark = root.classList.toggle('dark');
                localStorage.setItem(STORAGE_KEY, nowDark ? 'dark' : 'light');
            });
        });
    });
})();
