// ShirtVerse Custom JavaScript

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // 1. Smooth Scroll for Anchor Links
    // ========================================
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ========================================
    // 2. Auto-hide Alerts
    // ========================================
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // ========================================
    // 3. Form Validation Enhancement
    // ========================================
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // ========================================
    // 4. Navbar Scroll Effect
    // ========================================
    let lastScroll = 0;
    const navbar = document.querySelector('.navbar');
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 8px rgba(0,0,0,.2)';
        } else {
            navbar.style.boxShadow = '0 2px 4px rgba(0,0,0,.1)';
        }
        
        lastScroll = currentScroll;
    });

    // ========================================
    // 5. Product Image Lazy Loading
    // ========================================
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (img.dataset.src) {
                        img.src = img.dataset.src;
                        img.classList.remove('lazy');
                        observer.unobserve(img);
                    }
                }
            });
        });

        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }

    // ========================================
    // 6. Search Box Enhancement
    // ========================================
    const searchInput = document.querySelector('input[name="search"]');
    const suggestionContainer = document.querySelector('#search-suggestions');
    let activeSuggestionIndex = -1;
    if (searchInput) {
        searchInput.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        searchInput.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });

        if (suggestionContainer && searchInput.dataset.suggestionsUrl) {
            const suggestionsUrl = searchInput.dataset.suggestionsUrl;

            const hideSuggestions = () => {
                suggestionContainer.classList.add('d-none');
                suggestionContainer.innerHTML = '';
                activeSuggestionIndex = -1;
            };

            const renderSuggestions = results => {
                if (!results.length) {
                    hideSuggestions();
                    return;
                }
                suggestionContainer.innerHTML = results.map((item, index) => {
                    const priceLabel = item.price ? `₹${Number(item.price).toFixed(2)}` : '';
                    return `
                        <button type="button" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center" data-value="${item.name}" data-slug="${item.slug}" data-index="${index}">
                            <span>${item.name}</span>
                            <small class="text-muted ms-3">${priceLabel}</small>
                        </button>
                    `;
                }).join('');
                suggestionContainer.classList.remove('d-none');
                activeSuggestionIndex = -1;
            };

            const fetchSuggestions = debounce(async term => {
                if (term.length < 2) {
                    hideSuggestions();
                    return;
                }
                try {
                    const response = await fetch(`${suggestionsUrl}?q=${encodeURIComponent(term)}`);
                    if (!response.ok) {
                        hideSuggestions();
                        return;
                    }
                    const data = await response.json();
                    renderSuggestions(data.results || []);
                } catch (error) {
                    hideSuggestions();
                }
            }, 200);

            searchInput.addEventListener('input', event => {
                fetchSuggestions(event.target.value.trim());
            });

            suggestionContainer.addEventListener('click', event => {
                const button = event.target.closest('button[data-value]');
                if (!button) return;
                searchInput.value = button.dataset.value;
                hideSuggestions();
                searchInput.form && searchInput.form.requestSubmit();
            });

            searchInput.addEventListener('keydown', event => {
                const suggestions = suggestionContainer.querySelectorAll('button[data-value]');
                if (!suggestions.length) return;
                if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    activeSuggestionIndex = (activeSuggestionIndex + 1) % suggestions.length;
                } else if (event.key === 'ArrowUp') {
                    event.preventDefault();
                    activeSuggestionIndex = (activeSuggestionIndex - 1 + suggestions.length) % suggestions.length;
                } else if (event.key === 'Enter' && activeSuggestionIndex >= 0) {
                    event.preventDefault();
                    const selected = suggestions[activeSuggestionIndex];
                    selected.click();
                    return;
                } else if (event.key === 'Escape') {
                    hideSuggestions();
                    return;
                } else {
                    return;
                }

                suggestions.forEach(btn => btn.classList.remove('active'));
                suggestions[activeSuggestionIndex].classList.add('active');
            });

            document.addEventListener('click', event => {
                if (!suggestionContainer.contains(event.target) && event.target !== searchInput) {
                    hideSuggestions();
                }
            });
        }
    }

    // ========================================
    // 7. Quantity Selector
    // ========================================
    const quantityInputs = document.querySelectorAll('input[type="number"]');
    quantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            const value = parseInt(this.value);
            const min = parseInt(this.min) || 1;
            const max = parseInt(this.max) || Infinity;
            
            if (value < min) this.value = min;
            if (value > max) this.value = max;
        });
    });

    // ========================================
    // 8. Add to Cart Animation
    // ========================================
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Add success animation
            this.innerHTML = '<i class="bi bi-check"></i> Added!';
            this.classList.add('btn-success');
            this.disabled = true;
            
            setTimeout(() => {
                this.innerHTML = '<i class="bi bi-cart-plus"></i> Add to Cart';
                this.classList.remove('btn-success');
                this.disabled = false;
            }, 2000);
        });
    });

    // ========================================
    // 9. Price Filter Range
    // ========================================
    const minPrice = document.querySelector('input[name="min_price"]');
    const maxPrice = document.querySelector('input[name="max_price"]');
    
    if (minPrice && maxPrice) {
        minPrice.addEventListener('input', function() {
            if (maxPrice.value && parseInt(this.value) > parseInt(maxPrice.value)) {
                this.value = maxPrice.value;
            }
        });
        
        maxPrice.addEventListener('input', function() {
            if (minPrice.value && parseInt(this.value) < parseInt(minPrice.value)) {
                this.value = minPrice.value;
            }
        });
    }

    // ========================================
    // 10. Wishlist Toggle
    // ========================================
    const wishlistButtons = document.querySelectorAll('.wishlist-toggle');
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const icon = this.querySelector('i');
            if (icon.classList.contains('bi-heart')) {
                icon.classList.remove('bi-heart');
                icon.classList.add('bi-heart-fill');
                this.classList.add('text-danger');
            } else {
                icon.classList.remove('bi-heart-fill');
                icon.classList.add('bi-heart');
                this.classList.remove('text-danger');
            }
        });
    });

    // ========================================
    // 11. Product Card Fade In Animation
    // ========================================
    const productCards = document.querySelectorAll('.product-card');
    if (productCards.length > 0) {
        productCards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in');
            }, index * 100);
        });
    }

    // ========================================
    // 12. Toast Notifications
    // ========================================
    const toastElList = [].slice.call(document.querySelectorAll('.toast'));
    const toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 3000
        });
    });
    toastList.forEach(toast => toast.show());

    // ========================================
    // 13. Back to Top Button
    // ========================================
    const backToTopButton = document.createElement('button');
    backToTopButton.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTopButton.className = 'btn btn-primary back-to-top';
    backToTopButton.style.cssText = `
        position: fixed;
        bottom: 20px;
        right: 20px;
        display: none;
        z-index: 1000;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        padding: 0;
        box-shadow: 0 4px 8px rgba(0,0,0,.2);
    `;
    document.body.appendChild(backToTopButton);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    });

    backToTopButton.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    // ========================================
    // 14. Image Zoom on Product Detail
    // ========================================
    const productImages = document.querySelectorAll('.product-detail-image');
    productImages.forEach(img => {
        img.addEventListener('click', function() {
            const modal = new bootstrap.Modal(document.createElement('div'));
            // Create zoom modal if needed
        });
    });

    // ========================================
    // 15. Shopping Cart Counter Update
    // ========================================
    function updateCartCount() {
        const cartBadge = document.querySelector('.cart-badge');
        if (cartBadge) {
            // This would be updated via AJAX in a real scenario
            cartBadge.style.animation = 'pulse 0.5s';
        }
    }

    // ========================================
    // 16. Loading State for Forms
    // ========================================
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.classList.contains('no-loading')) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
                submitBtn.disabled = true;
            }
        });
    });

    // ========================================
    // 17. Star Rating Interactive
    // ========================================
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                stars.forEach((s, i) => {
                    if (i <= index) {
                        s.classList.add('active');
                    } else {
                        s.classList.remove('active');
                    }
                });
            });
        });
    });

    // ========================================
    // 18. Confirm Delete Actions
    // ========================================
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', function(e) {
            const message = this.dataset.confirm || 'Are you sure?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // ========================================
    // 19. Password Visibility Toggle
    // ========================================
    const passwordToggles = document.querySelectorAll('.password-toggle');
    passwordToggles.forEach(toggle => {
        toggle.addEventListener('click', function() {
            const input = this.previousElementSibling;
            const icon = this.querySelector('i');
            
            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('bi-eye');
                icon.classList.add('bi-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('bi-eye-slash');
                icon.classList.add('bi-eye');
            }
        });
    });

    // ========================================
    // 20. Print Invoice
    // ========================================
    const printButtons = document.querySelectorAll('.print-invoice');
    printButtons.forEach(button => {
        button.addEventListener('click', () => {
            window.print();
        });
    });

});

// ========================================
// Utility Functions
// ========================================

// Show Toast Notification
function showToast(message, type = 'info') {
    const toastContainer = document.querySelector('.toast-container') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type} border-0`;
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toast);
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
    toast.addEventListener('hidden.bs.toast', () => toast.remove());
}

// Create Toast Container
function createToastContainer() {
    const container = document.createElement('div');
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    document.body.appendChild(container);
    return container;
}

// Format Currency
function formatCurrency(amount) {
    return '₹' + parseFloat(amount).toFixed(2);
}

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}
