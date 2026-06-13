// static/js/main.js

// Sidebar toggle
document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
    }
    
    // Close modal
    const modalClose = document.getElementById('modalClose');
    const modalOverlay = document.getElementById('modalOverlay');
    
    if (modalClose) {
        modalClose.addEventListener('click', closeModal);
    }
    
    if (modalOverlay) {
        modalOverlay.addEventListener('click', function(e) {
            if (e.target === e.currentTarget) closeModal();
        });
    }
});


function closeModal() {
    const modalOverlay = document.getElementById('modalOverlay');
    if (modalOverlay) modalOverlay.classList.remove('open');
}

function openModal(title, content) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalTitle = document.getElementById('modalTitle');
    const modalBody = document.getElementById('modalBody');
    
    if (modalTitle) modalTitle.textContent = title;
    if (modalBody) modalBody.innerHTML = content;
    if (modalOverlay) modalOverlay.classList.add('open');
}

// Table filter
function filterTable(input, tableId) {
    const q = input.value.toLowerCase();
    const rows = document.querySelectorAll('#' + tableId + ' tbody tr');
    rows.forEach(function(row) {
        row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
}

// Color generator for avatars
const COLORS = [
    '#4f6ef7','#22c55e','#f59e0b','#ef4444',
    '#8b5cf6','#06b6d4','#f97316','#ec4899',
    '#14b8a6','#6366f1','#84cc16','#e879f9'
];

function colorFor(name) {
    let h = 0;
    for (const c of name) h = (h * 31 + c.charCodeAt(0)) & 0xffffffff;
    return COLORS[Math.abs(h) % COLORS.length];
}

function initials(name) {
    return name.split(' ').slice(0,2).map(w => w[0]).join('').toUpperCase();
}

function avatarCell(name, sub) {
    const col = colorFor(name);
    return `
        <div class="user-cell">
            <div class="cell-ava" style="background:${col}">${initials(name)}</div>
            <div>
                <div class="cell-name">${name}</div>
                ${sub ? `<div class="cell-email">${sub}</div>` : ''}
            </div>
        </div>`;
}

function pill(text, cls) {
    return `<span class="pill ${cls}">${text}</span>`;
}

function actionBtns(viewUrl, editUrl, deleteUrl) {
    return `
        <div class="action-btns">
            <a href="${viewUrl}" class="act-btn" title="View"><i class="bi bi-eye"></i></a>
            <a href="${editUrl}" class="act-btn" title="Edit"><i class="bi bi-pencil"></i></a>
            <a href="${deleteUrl}" class="act-btn danger" title="Delete"><i class="bi bi-trash"></i></a>
        </div>`;
}