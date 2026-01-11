// BloodConnect Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    
                    // Create error message if not exists
                    if (!field.nextElementSibling?.classList.contains('invalid-feedback')) {
                        const errorDiv = document.createElement('div');
                        errorDiv.className = 'invalid-feedback';
                        errorDiv.textContent = 'This field is required';
                        field.parentNode.appendChild(errorDiv);
                    }
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = this.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
    });

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[name="phone"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 10) value = value.substring(0, 10);
            
            // Format as (123) 456-7890
            if (value.length > 6) {
                value = `(${value.substring(0,3)}) ${value.substring(3,6)}-${value.substring(6)}`;
            } else if (value.length > 3) {
                value = `(${value.substring(0,3)}) ${value.substring(3)}`;
            } else if (value.length > 0) {
                value = `(${value}`;
            }
            
            e.target.value = value;
        });
    });

    // Copy to clipboard functionality
    const copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(button => {
        button.addEventListener('click', function() {
            const textToCopy = this.getAttribute('data-copy') || 
                              this.previousElementSibling?.value || 
                              this.previousElementSibling?.textContent;
            
            if (textToCopy) {
                navigator.clipboard.writeText(textToCopy).then(() => {
                    const originalText = this.innerHTML;
                    this.innerHTML = '<i class="bi bi-check"></i> Copied!';
                    this.classList.remove('btn-outline-secondary');
                    this.classList.add('btn-success');
                    
                    setTimeout(() => {
                        this.innerHTML = originalText;
                        this.classList.remove('btn-success');
                        this.classList.add('btn-outline-secondary');
                    }, 2000);
                });
            }
        });
    });

    // Blood group selector enhancement
    const bloodGroupSelects = document.querySelectorAll('select[name="blood_group"]');
    bloodGroupSelects.forEach(select => {
        // Add color coding to options
        const options = select.querySelectorAll('option');
        options.forEach(option => {
            if (option.value) {
                option.style.fontWeight = 'bold';
                switch(option.value) {
                    case 'A+': option.style.color = '#dc3545'; break;
                    case 'A-': option.style.color = '#fd7e14'; break;
                    case 'B+': option.style.color = '#28a745'; break;
                    case 'B-': option.style.color = '#20c997'; break;
                    case 'AB+': option.style.color = '#6f42c1'; break;
                    case 'AB-': option.style.color = '#e83e8c'; break;
                    case 'O+': option.style.color = '#007bff'; break;
                    case 'O-': option.style.color = '#17a2b8'; break;
                }
            }
        });
    });

    // Stock quantity validation
    const stockInputs = document.querySelectorAll('input[name*="quantity"]');
    stockInputs.forEach(input => {
        input.addEventListener('change', function() {
            const value = parseInt(this.value);
            if (value < 0) {
                this.value = 0;
                alert('Quantity cannot be negative');
            }
            if (value > 1000) {
                this.value = 1000;
                alert('Maximum quantity is 1000 units');
            }
        });
    });

    // Price validation
    const priceInputs = document.querySelectorAll('input[name*="price"]');
    priceInputs.forEach(input => {
        input.addEventListener('change', function() {
            const value = parseFloat(this.value);
            if (value < 0) {
                this.value = 0;
                alert('Price cannot be negative');
            }
        });
    });

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
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

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    console.log('BloodConnect JavaScript loaded successfully');
});
