document.addEventListener('DOMContentLoaded', function() {
    // Sidebar toggle
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }
    
    // Footer menu toggle
    const userMenuToggle = document.getElementById('userMenuToggle');
    const footerMenu = document.getElementById('footerMenu');
    const userChevron = document.getElementById('userChevron');
    
    if (userMenuToggle && footerMenu) {
        userMenuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            const isOpen = footerMenu.classList.contains('show');
            
            if (isOpen) {
                userMenuToggle.classList.remove('active');
                footerMenu.classList.remove('show');
                if (userChevron) userChevron.classList.replace('bi-chevron-down', 'bi-chevron-up');
            } else {
                userMenuToggle.classList.add('active');
                footerMenu.classList.add('show');
                if (userChevron) userChevron.classList.replace('bi-chevron-up', 'bi-chevron-down');
            }
        });
        
        document.addEventListener('click', function(e) {
            if (!userMenuToggle.contains(e.target) && !footerMenu.contains(e.target)) {
                userMenuToggle.classList.remove('active');
                footerMenu.classList.remove('show');
                if (userChevron) userChevron.classList.replace('bi-chevron-down', 'bi-chevron-up');
            }
        });
    }
    
    // Load dark mode preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateDarkModeUI(true);
    }
    
    // Logout modal
    const logoutModalOverlay = document.getElementById('logoutModalOverlay');
    if (logoutModalOverlay) {
        logoutModalOverlay.addEventListener('click', function(e) {
            if (e.target === e.currentTarget) hideLogoutModal();
        });
    }
});

// Dark Mode
function toggleDarkMode() {
    const html = document.documentElement;
    const isDark = html.getAttribute('data-theme') === 'dark';
    
    if (isDark) {
        html.removeAttribute('data-theme');
        localStorage.setItem('theme', 'light');
        updateDarkModeUI(false);
    } else {
        html.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        updateDarkModeUI(true);
    }
}

function updateDarkModeUI(isDark) {
    const icon = document.getElementById('darkModeIcon');
    const text = document.getElementById('darkModeText');
    
    if (icon && text) {
        if (isDark) {
            icon.classList.replace('bi-moon-fill', 'bi-sun-fill');
            text.textContent = 'Light Mode';
        } else {
            icon.classList.replace('bi-sun-fill', 'bi-moon-fill');
            text.textContent = 'Dark Mode';
        }
    }
}

function showLogoutModal() {
    const modal = document.getElementById('logoutModalOverlay');
    if (modal) modal.classList.add('open');
    
    const userMenuToggle = document.getElementById('userMenuToggle');
    const footerMenu = document.getElementById('footerMenu');
    const userChevron = document.getElementById('userChevron');
    if (userMenuToggle) userMenuToggle.classList.remove('active');
    if (footerMenu) footerMenu.classList.remove('show');
    if (userChevron) userChevron.classList.replace('bi-chevron-down', 'bi-chevron-up');
}

function hideLogoutModal() {
    const modal = document.getElementById('logoutModalOverlay');
    if (modal) modal.classList.remove('open');
}

function filterTable(input, tableId) {
    const q = input.value.toLowerCase();
    const rows = document.querySelectorAll('#' + tableId + ' tbody tr');
    rows.forEach(function(row) {
        row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
}