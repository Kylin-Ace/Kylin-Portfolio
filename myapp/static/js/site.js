function initializeNavigation() {
    const menuButton = document.getElementById("mobileMenuBtn");
    const mobileMenu = document.getElementById("mobileMenu");
    const mobileThemeToggle = document.getElementById("mobileThemeToggle");
    const themeToggle = document.getElementById("themeToggle");

    if (menuButton && mobileMenu) {
        menuButton.addEventListener("click", () => {
            const isExpanded = menuButton.getAttribute("aria-expanded") === "true";
            menuButton.setAttribute("aria-expanded", String(!isExpanded));
            menuButton.setAttribute("aria-label", isExpanded ? "Open navigation menu" : "Close navigation menu");
            mobileMenu.classList.toggle("hidden", isExpanded);
        });
    }

    if (mobileThemeToggle && themeToggle) {
        mobileThemeToggle.addEventListener("click", () => themeToggle.click());
    }
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initializeNavigation, { once: true });
} else {
    initializeNavigation();
}
