// Close message alerts
document.addEventListener('DOMContentLoaded', function() {
    const closeButtons = document.querySelectorAll('.close-message');
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.parentElement.style.display = 'none';
        });
    });

    // Auto-hide messages after 5 seconds
    const messages = document.querySelectorAll('.message');
    messages.forEach(message => {
        setTimeout(() => {
            message.style.transition = 'opacity 0.3s';
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Mobile side panel toggle
    const mobileUserToggle = document.getElementById('mobileUserToggle');
    const mobileSidePanel = document.getElementById('mobileSidePanel');
    const mobilePanelOverlay = document.getElementById('mobilePanelOverlay');
    const mobilePanelClose = document.getElementById('mobilePanelClose');
    const body = document.body;

    function openMobilePanel() {
        if (mobileSidePanel) {
            mobileSidePanel.classList.add('open');
            if (mobileUserToggle) {
                mobileUserToggle.classList.add('active');
                mobileUserToggle.setAttribute('aria-expanded', 'true');
            }
            body.classList.add('mobile-panel-open');
        }
    }

    function closeMobilePanel() {
        if (mobileSidePanel) {
            mobileSidePanel.classList.remove('open');
            if (mobileUserToggle) {
                mobileUserToggle.classList.remove('active');
                mobileUserToggle.setAttribute('aria-expanded', 'false');
            }
            body.classList.remove('mobile-panel-open');
        }
    }

    if (mobileUserToggle && mobileSidePanel) {
        mobileUserToggle.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (mobileSidePanel.classList.contains('open')) {
                closeMobilePanel();
            } else {
                openMobilePanel();
            }
        });
    }

    if (mobilePanelClose) {
        mobilePanelClose.addEventListener('click', function(e) {
            e.preventDefault();
            closeMobilePanel();
        });
    }

    if (mobilePanelOverlay) {
        mobilePanelOverlay.addEventListener('click', function() {
            closeMobilePanel();
        });
    }

    // Close panel when clicking outside on mobile
    document.addEventListener('click', function(e) {
        if (mobileSidePanel && mobileSidePanel.classList.contains('open')) {
            if (!mobileSidePanel.contains(e.target) && 
                mobileUserToggle && !mobileUserToggle.contains(e.target)) {
                closeMobilePanel();
            }
        }
    });

    // Close panel on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && mobileSidePanel && mobileSidePanel.classList.contains('open')) {
            closeMobilePanel();
        }
    });

    // Close panel when clicking on nav links
    if (mobileSidePanel) {
        const navLinks = mobileSidePanel.querySelectorAll('.mobile-panel-nav a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                // Close panel after a short delay to allow navigation
                setTimeout(() => {
                    closeMobilePanel();
                }, 100);
            });
        });
    }

    // Handle window resize - close panel if resizing to desktop
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768 && mobileSidePanel && mobileSidePanel.classList.contains('open')) {
            closeMobilePanel();
        }
    });

    // Dropdown toggle on desktop (hover)
    function enableDesktopDropdowns() {
        const dropdownToggles = document.querySelectorAll('.dropdown > .dropdown-toggle');
        dropdownToggles.forEach(toggle => {
            // Only enable click for desktop if needed
            if (window.innerWidth > 768) {
                toggle.addEventListener('click', function(e) {
                    // Allow default behavior on desktop for accessibility
                });
            }
        });
    }

    enableDesktopDropdowns();
});

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.style.borderColor = '#dc3545';
        } else {
            field.style.borderColor = '';
        }
    });

    return isValid;
}

// Image preview for product forms
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('image-preview');
            if (preview) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            }
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Quantity validation
function validateQuantity(input) {
    const min = parseInt(input.getAttribute('min')) || 1;
    const max = parseInt(input.getAttribute('max')) || 999;
    let value = parseInt(input.value) || min;

    if (value < min) {
        value = min;
    } else if (value > max) {
        value = max;
    }

    input.value = value;
}

// Smooth scroll
function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({
        behavior: 'smooth'
    });
}

