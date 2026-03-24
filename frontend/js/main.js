// ==================== PWA Installation ==================== 
let deferredPrompt;

// ==================== Routing Helpers ====================
const STATIC_PORTS = new Set(['5500', '5501', '5502', '5503']);
const isStaticMode = window.location.protocol === 'file:' || STATIC_PORTS.has(window.location.port);

function pageUrl(name) {
    const pageMap = {
        index: 'index.html',
        login: 'login.html',
        signup: 'signup.html',
        form: 'form.html',
        result: 'result.html'
    };

    if (isStaticMode) {
        return pageMap[name] || pageMap.index;
    }

    return name === 'index' ? '/' : `/${name}`;
}

function apiUrl(path) {
    return isStaticMode ? `http://127.0.0.1:5000${path}` : path;
}

window.ObesiCareRouter = {
    isStaticMode,
    page: pageUrl,
    api: apiUrl
};

// Listen for the beforeinstallprompt event
window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent the mini-infobar from appearing on mobile
    e.preventDefault();
    // Stash the event for later use
    deferredPrompt = e;
    // Show the install prompt
    showInstallPrompt();
});

function showInstallPrompt() {
    const installPrompt = document.getElementById('installPrompt');
    if (installPrompt) {
        installPrompt.classList.remove('hidden');
    }
}

function hideInstallPrompt() {
    const installPrompt = document.getElementById('installPrompt');
    if (installPrompt) {
        installPrompt.classList.add('hidden');
    }
}

// Install button click handler
const installBtn = document.getElementById('installBtn');
if (installBtn) {
    installBtn.addEventListener('click', async () => {
        if (deferredPrompt) {
            // Show the install prompt
            deferredPrompt.prompt();
            // Wait for the user to respond to the prompt
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to the install prompt: ${outcome}`);
            // We won't need the prompt anymore
            deferredPrompt = null;
            hideInstallPrompt();
        }
    });
}

// Dismiss button click handler
const dismissBtn = document.getElementById('dismissBtn');
if (dismissBtn) {
    dismissBtn.addEventListener('click', hideInstallPrompt);
}

// Auto-hide install prompt after 5 seconds if user doesn't interact
setTimeout(() => {
    const installPrompt = document.getElementById('installPrompt');
    if (installPrompt && !installPrompt.classList.contains('hidden')) {
        // Optional: auto-hide after a delay (comment out if you want it persistent)
        // hideInstallPrompt();
    }
}, 5000);

// ==================== Service Worker Registration ==================== 
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        // Register the PWA service worker from app root.
        navigator.serviceWorker.register('/sw.js')
            .then(reg => console.log('Service Worker registered'))
            .catch(err => console.log('Service Worker registration failed:', err));
    });
}

// ==================== Navigation ==================== 
const startBtns = document.querySelectorAll('#startBtn, #heroStartBtn');
startBtns.forEach(btn => {
    if (btn) {
        btn.addEventListener('click', (e) => {
            e.preventDefault();
            // Required flow: landing page should always enter through login.
            window.location.href = pageUrl('login');
        });
    }
});

// ==================== Smooth Scroll ==================== 
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href !== '#' && href !== '#home') {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        }
    });
});

// ==================== Form Utilities ==================== 
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function formatHeight(meters) {
    return Math.round(meters * 100) / 100;
}

function calculateBMI(weight, height) {
    if (height === 0) return 0;
    return Math.round((weight / (height * height)) * 100) / 100;
}

// ==================== Session Management ==================== 
class SessionManager {
    static saveUsername(username) {
        localStorage.setItem('username', username);
    }

    static getUsername() {
        return localStorage.getItem('username');
    }

    static clearUsername() {
        localStorage.removeItem('username');
    }

    static isLoggedIn() {
        return !!this.getUsername();
    }
}

// ==================== API Utilities ==================== 
class APIClient {
    static async post(endpoint, data) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error(`API Error: ${error}`);
            throw error;
        }
    }

    static async get(endpoint) {
        try {
            const response = await fetch(endpoint);
            return await response.json();
        } catch (error) {
            console.error(`API Error: ${error}`);
            throw error;
        }
    }
}

// ==================== Notification System ==================== 
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

// ==================== Dark Mode Toggle ==================== 
function initializeDarkMode() {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedDarkMode = localStorage.getItem('darkMode');
    
    if (savedDarkMode !== null) {
        if (savedDarkMode === 'true') {
            document.body.classList.add('dark-mode');
        }
    } else if (prefersDark) {
        document.body.classList.add('dark-mode');
    }
}

// ==================== Accessibility ==================== 
// Add keyboard navigation support
document.addEventListener('keydown', (e) => {
    // Escape key - close modals or dropdowns if implemented
    if (e.key === 'Escape') {
        hideInstallPrompt();
    }
    
    // Alt + L - Quick logout
    if (e.altKey && e.key.toLowerCase() === 'l') {
        const logoutBtn = document.getElementById('logoutBtn');
        if (logoutBtn) {
            logoutBtn.click();
        }
    }
});

// ==================== Performance Monitoring ==================== 
function logPageMetrics() {
    if (window.performance && window.performance.timing) {
        const timing = window.performance.timing;
        const loadTime = timing.loadEventEnd - timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

window.addEventListener('load', logPageMetrics);

// ==================== Error Handling ==================== 
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
    // You could send this to an error tracking service
});

window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
    // You could send this to an error tracking service
});

// ==================== Utility Functions ==================== 
const Utils = {
    // Debounce function for performance
    debounce(func, delay) {
        let timeoutId;
        return function (...args) {
            clearTimeout(timeoutId);
            timeoutId = setTimeout(() => func(...args), delay);
        };
    },

    // Throttle function for scroll events
    throttle(func, limit) {
        let inThrottle;
        return function (...args) {
            if (!inThrottle) {
                func(...args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Format date
    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(date);
    },

    // Format number with commas
    formatNumber(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },

    // localStorage operations
    storage: {
        set(key, value) {
            try {
                localStorage.setItem(key, JSON.stringify(value));
                return true;
            } catch (e) {
                console.error('Storage error:', e);
                return false;
            }
        },
        get(key) {
            try {
                const item = localStorage.getItem(key);
                return item ? JSON.parse(item) : null;
            } catch (e) {
                console.error('Storage error:', e);
                return null;
            }
        },
        remove(key) {
            try {
                localStorage.removeItem(key);
                return true;
            } catch (e) {
                console.error('Storage error:', e);
                return false;
            }
        },
        clear() {
            try {
                localStorage.clear();
                return true;
            } catch (e) {
                console.error('Storage error:', e);
                return false;
            }
        }
    }
};

// ==================== Scroll to Top Button ==================== 
function initializeScrollToTop() {
    const scrollBtn = document.createElement('button');
    scrollBtn.innerHTML = '⬆️';
    scrollBtn.id = 'scrollToTop';
    scrollBtn.className = 'scroll-to-top';
    scrollBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        background: linear-gradient(135deg, #2ecc71, #3498db);
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 1.5rem;
        cursor: pointer;
        display: none;
        z-index: 99;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    `;

    document.body.appendChild(scrollBtn);

    window.addEventListener('scroll', () => {
        if (document.documentElement.scrollTop > 300) {
            scrollBtn.style.display = 'block';
        } else {
            scrollBtn.style.display = 'none';
        }
    });

    scrollBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    scrollBtn.addEventListener('mouseover', () => {
        scrollBtn.style.transform = 'scale(1.1)';
    });

    scrollBtn.addEventListener('mouseout', () => {
        scrollBtn.style.transform = 'scale(1)';
    });
}

// Initialize on page load
window.addEventListener('DOMContentLoaded', () => {
    initializeDarkMode();
    initializeScrollToTop();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        SessionManager,
        APIClient,
        Utils
    };
}
