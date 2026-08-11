// PrajaConnectAI Modern Citizen Platform JavaScript Engine

document.addEventListener('DOMContentLoaded', () => {
    initVoiceSearch();
    initTheme();
    initNotifications();
    initBottomSheetGestures();
});

// Theme Management (Persisted in localStorage)
function initTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
}

function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
    showToast(`Switched to ${newTheme} mode`);
}

function updateThemeIcon(theme) {
    const themeIcon = document.getElementById('themeIcon');
    if (!themeIcon) return;
    if (theme === 'dark') {
        themeIcon.className = 'bi bi-moon-stars-fill text-warning';
    } else {
        themeIcon.className = 'bi bi-sun-fill';
    }
}

// Notification Drawer management
function initNotifications() {
    const badge = document.getElementById('notiBadge');
    if (badge) {
        // Set sample count of unread notifications
        badge.innerText = '3';
    }
}

function openNotificationDrawer() {
    const overlay = document.getElementById('notificationOverlay');
    const sheet = document.getElementById('notificationBottomSheet');
    if (overlay && sheet) {
        overlay.classList.add('active');
        sheet.classList.add('active');
    }
}

function closeNotificationDrawer() {
    const overlay = document.getElementById('notificationOverlay');
    const sheet = document.getElementById('notificationBottomSheet');
    if (overlay && sheet) {
        overlay.classList.remove('active');
        sheet.classList.remove('active');
    }
    // Clear badge count upon viewing
    const badge = document.getElementById('notiBadge');
    if (badge) badge.innerText = '';
}

// Location Selector Modal
function openLocationModal() {
    const modal = document.getElementById('locationModal');
    if (modal) modal.classList.add('active');
}

function closeLocationModal() {
    const modal = document.getElementById('locationModal');
    if (modal) modal.classList.remove('active');
}

function changeLocation(city) {
    const label = document.getElementById('headerLocationText');
    if (label) {
        label.innerText = city + ", AP";
    }
    closeLocationModal();
    showToast(`Location set to ${city}`);
    
    // Automatically submit any filter form on the page if present
    const districtSelect = document.querySelector('select[name="district"]');
    if (districtSelect) {
        districtSelect.value = city;
        districtSelect.form.submit();
    } else {
        // Reload page to reflect context if needed, or update session via ajax if we want
        localStorage.setItem('user_location', city);
    }
}

// Bottom Sheet Component Actions
function openBottomSheet(title, htmlContent) {
    const titleEl = document.getElementById('bottomSheetTitle');
    const contentEl = document.getElementById('bottomSheetContent');
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('detailBottomSheet');
    
    if (titleEl && contentEl && overlay && sheet) {
        titleEl.innerText = title;
        contentEl.innerHTML = htmlContent;
        overlay.classList.add('active');
        sheet.classList.add('active');
    }
}

function closeBottomSheet() {
    const overlay = document.getElementById('bottomSheetOverlay');
    const sheet = document.getElementById('detailBottomSheet');
    if (overlay && sheet) {
        overlay.classList.remove('active');
        sheet.classList.remove('active');
    }
}

// Swipe / Drag gestures to close bottom sheets
function initBottomSheetGestures() {
    const sheet = document.getElementById('detailBottomSheet');
    const handle = document.getElementById('sheetDragHandle');
    if (!sheet || !handle) return;
    
    let startY = 0;
    let currentY = 0;
    let isDragging = false;
    
    handle.addEventListener('touchstart', (e) => {
        startY = e.touches[0].clientY;
        isDragging = true;
        sheet.style.transition = 'none';
    });
    
    handle.addEventListener('touchmove', (e) => {
        if (!isDragging) return;
        currentY = e.touches[0].clientY;
        const deltaY = currentY - startY;
        if (deltaY > 0) {
            sheet.style.transform = `translateY(${deltaY}px)`;
        }
    });
    
    handle.addEventListener('touchend', (e) => {
        if (!isDragging) return;
        isDragging = false;
        sheet.style.transition = 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
        const deltaY = currentY - startY;
        if (deltaY > 120) {
            closeBottomSheet();
        }
        sheet.style.transform = '';
    });
}

// Floating AI Panel Interactions
function toggleFloatingAi() {
    const panel = document.getElementById('floatingAiPanel');
    if (panel) {
        panel.classList.toggle('active');
        if (panel.classList.contains('active')) {
            const input = document.getElementById('floatingAiInput');
            if (input) input.focus();
        }
    }
}

function sendSuggestedQuery(text) {
    const input = document.getElementById('floatingAiInput');
    if (input) {
        input.value = text;
        const form = document.getElementById('floatingAiForm');
        if (form) {
            const event = new Event('submit', { cancelable: true, bubbles: true });
            form.dispatchEvent(event);
        }
    }
}

function handleFloatingAiSubmit(event) {
    event.preventDefault();
    const input = document.getElementById('floatingAiInput');
    const messagesContainer = document.getElementById('floatingAiMessages');
    
    if (!input || !messagesContainer) return;
    
    const queryText = input.value.trim();
    if (!queryText) return;
    
    // Add user bubble
    appendMessageBubble(messagesContainer, 'user', queryText);
    input.value = '';
    
    // Add loading skeleton bubble
    const loadingId = 'ai-loading-' + Date.now();
    const loadingBubble = document.createElement('div');
    loadingBubble.id = loadingId;
    loadingBubble.className = 'message-bubble msg-ai skeleton';
    loadingBubble.innerHTML = `<div class="skeleton-line" style="width: 80px;"></div>`;
    messagesContainer.appendChild(loadingBubble);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    // Connect to existing AI backend endpoint
    fetch('/assistant/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: queryText })
    })
    .then(res => res.json())
    .then(data => {
        // Remove loading bubble
        const bubble = document.getElementById(loadingId);
        if (bubble) bubble.remove();
        
        if (data.success) {
            appendMessageBubble(messagesContainer, 'ai', data.response);
        } else {
            appendMessageBubble(messagesContainer, 'ai', 'Unable to retrieve answer. Please try again.');
        }
    })
    .catch(err => {
        const bubble = document.getElementById(loadingId);
        if (bubble) bubble.remove();
        appendMessageBubble(messagesContainer, 'ai', 'Network error. Please check your connection.');
        console.error('AI chat failed:', err);
    });
}

function appendMessageBubble(container, role, text) {
    const bubble = document.createElement('div');
    bubble.className = `message-bubble msg-${role}`;
    // Replace newlines with breaks
    bubble.innerHTML = text.replace(/\n/g, '<br>');
    container.appendChild(bubble);
    container.scrollTop = container.scrollHeight;
}

// Web Speech API Voice Search Implementation
function initVoiceSearch() {
    const micBtn = document.getElementById('micSearchBtn');
    const searchInput = document.getElementById('searchInput');

    if (!micBtn || !searchInput) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        micBtn.addEventListener('click', () => {
            if (micBtn.classList.contains('listening')) {
                recognition.stop();
            } else {
                try {
                    recognition.start();
                } catch (e) {
                    console.error('Speech recognition error:', e);
                }
            }
        });

        recognition.onstart = () => {
            micBtn.classList.add('listening');
            searchInput.placeholder = "Listening... Speak now";
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
            micBtn.classList.remove('listening');
            searchInput.placeholder = "Search schemes, camps, services...";
            if (searchInput.form) {
                searchInput.form.submit();
            }
        };

        recognition.onerror = (event) => {
            console.warn('Speech recognition error event:', event.error);
            micBtn.classList.remove('listening');
            searchInput.placeholder = "Search schemes, camps, services...";
            showToast("Voice input error. Please try typing.");
        };

        recognition.onend = () => {
            micBtn.classList.remove('listening');
            searchInput.placeholder = "Search schemes, camps, services...";
        };
    } else {
        micBtn.addEventListener('click', () => {
            showToast("Voice search is not supported on this browser.");
        });
    }
}

// Modal Handlers
function openLangModal() {
    const modal = document.getElementById('langModal');
    if (modal) modal.classList.add('active');
}

function closeLangModal() {
    const modal = document.getElementById('langModal');
    if (modal) modal.classList.remove('active');
}

function openQRModal() {
    const modal = document.getElementById('qrModal');
    if (modal) modal.classList.add('active');
}

function closeQRModal() {
    const modal = document.getElementById('qrModal');
    if (modal) modal.classList.remove('active');
}

// Change Application Language via fetch
function selectLanguage(lang) {
    fetch('/set_language', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: lang })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            window.location.reload();
        }
    })
    .catch(err => {
        console.error('Failed to change language:', err);
    });
}

// Toast notification function
function showToast(message) {
    let container = document.getElementById('toastContainer');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toastContainer';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.style.background = 'var(--text-primary)';
    toast.style.color = 'var(--bg-card)';
    toast.style.padding = '12px 20px';
    toast.style.borderRadius = '12px';
    toast.style.boxShadow = 'var(--shadow-md)';
    toast.style.marginBottom = '10px';
    toast.style.fontSize = '0.85rem';
    toast.style.fontWeight = '700';
    toast.style.animation = 'fadeIn 0.3s ease';
    toast.innerHTML = `<i class="bi bi-info-circle-fill text-primary" style="margin-right: 8px;"></i>${message}`;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transition = 'opacity 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Generic Quick Services action handlers
function handleQuickAction(actionType) {
    switch (actionType) {
        case 'search_schemes':
            window.location.href = '/schemes';
            break;
        case 'check_eligibility':
            window.location.href = '/assistant?q=' + encodeURIComponent('How to check my eligibility for government schemes?');
            break;
        case 'required_documents':
            window.location.href = '/assistant?q=' + encodeURIComponent('What general documents are required for government schemes?');
            break;
        case 'nearby_centers':
            window.location.href = '/camps';
            break;
        case 'check_updates':
            openNotificationDrawer();
            break;
        case 'grievance_redressal':
            showToast("Grievance Redressal: Call 1800-11-0001 or visit pgportal.gov.in");
            break;
        case 'helpline_support':
            showToast("Toll-Free National Helpline: 1800-11-2026");
            break;
        case 'nearby_support':
            window.location.href = '/camps';
            break;
        default:
            showToast("Service selected: " + actionType);
    }
}
