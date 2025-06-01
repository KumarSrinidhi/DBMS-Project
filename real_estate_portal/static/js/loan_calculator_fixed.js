/**
 * Loan Calculator - Main JavaScript
 * Optimized for performance and user experience
 */

// Wait for DOM to be fully loaded before initializing
document.addEventListener('DOMContentLoaded', function() {
    // Cache DOM elements
    const loanForm = document.getElementById('loanForm');
    const loanAmount = document.getElementById('loanAmount');
    const interestRate = document.getElementById('interestRate');
    const loanTerm = document.getElementById('loanTerm');
    const downPayment = document.getElementById('downPayment');
    const submitButton = loanForm?.querySelector('button[type="submit"]');
    const buttonText = submitButton?.querySelector('.button-text');
    const loadingSpinner = submitButton?.querySelector('.loading');
    const resultsSection = document.getElementById('loanResults');
    
    // ===== Form Submission Handler =====
    if (loanForm) {
        loanForm.addEventListener('submit', function(event) {
            if (!validateForm()) {
                // Prevent submission if validation fails
                event.preventDefault();
                return false;
            }
            
            // Show loading state
            showLoading(true);
        });
    }

    // ===== Input Formatting and Validation =====
    if (loanAmount && downPayment) {
        // Apply number formatting on blur and validate on input
        [loanAmount, downPayment].forEach(input => {
            input.addEventListener('blur', formatNumberInput);
            input.addEventListener('input', validateNumericInput);
        });
    }

    if (interestRate) {
        interestRate.addEventListener('input', validateNumericInput);
        interestRate.addEventListener('blur', function() {
            // Format interest rate to 2 decimal places on blur
            if (this.value && !isNaN(this.value)) {
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    }
    
    if (loanTerm) {
        loanTerm.addEventListener('input', validateNumericInput);
    }
    
    // Animate results section elements if they exist
    animateResultsSection();
    
    // Initialize dynamic input handlers
    setupInputHandlers();
    
    // ===== Helper Functions =====
    
    /**
     * Validates the loan calculator form
     * @returns {boolean} - Whether form is valid
     */
    function validateForm() {
        let isValid = true;
        
        // Check loan amount
        if (loanAmount) {
            const amount = parseFloat(loanAmount.value.replace(/,/g, ''));
            if (isNaN(amount) || amount < 100000) {
                showError(loanAmount, 'Please enter a valid loan amount (minimum ₹1,00,000)');
                isValid = false;
            } else {
                removeError(loanAmount);
            }
        }
        
        // Check interest rate
        if (interestRate) {
            const rate = parseFloat(interestRate.value);
            if (isNaN(rate) || rate < 1 || rate > 30) {
                showError(interestRate, 'Please enter a valid interest rate between 1% and 30%');
                isValid = false;
            } else {
                removeError(interestRate);
            }
        }
        
        // Check loan term
        if (loanTerm) {
            const term = parseInt(loanTerm.value);
            if (isNaN(term) || term < 1 || term > 30) {
                showError(loanTerm, 'Please enter a valid loan term between 1 and 30 years');
                isValid = false;
            } else {
                removeError(loanTerm);
            }
        }
        
        // Check down payment if provided
        if (downPayment && downPayment.value.trim() !== '') {
            const paymentAmount = parseFloat(downPayment.value.replace(/,/g, ''));
            const loanTotal = parseFloat(loanAmount.value.replace(/,/g, ''));
            
            if (isNaN(paymentAmount) || paymentAmount < 0) {
                showError(downPayment, 'Please enter a valid down payment amount');
                isValid = false;
            } else if (paymentAmount >= loanTotal) {
                showError(downPayment, 'Down payment cannot be greater than or equal to the loan amount');
                isValid = false;
            } else {
                removeError(downPayment);
            }
        }
        
        return isValid;
    }
    
    /**
     * Formats number input with thousand separators
     */
    function formatNumberInput() {
        if (this.value && this.name !== 'rate' && this.name !== 'tenure') {
            const num = parseFloat(this.value.replace(/,/g, ''));
            if (!isNaN(num)) {
                this.value = num.toLocaleString('en-IN');
            }
        }
    }
    
    /**
     * Validates that input contains only numeric characters
     */
    function validateNumericInput(e) {
        // Allow: backspace, delete, tab, escape, enter, decimal point, and comma
        const allowedKeys = [8, 9, 27, 13, 110, 190, 188];
        
        // Allow navigation keys
        if (allowedKeys.includes(e.keyCode) || 
            // Allow: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
            (e.keyCode >= 35 && e.keyCode <= 40) || 
            ((e.keyCode === 65 || e.keyCode === 67 || e.keyCode === 86 || e.keyCode === 88) && e.ctrlKey === true)) {
            return;
        }
        
        // Remove non-numeric characters except decimal point
        this.value = this.value.replace(/[^\d.]/g, '');
        
        // Ensure only one decimal point
        const decimalPoints = (this.value.match(/\./g) || []).length;
        if (decimalPoints > 1) {
            this.value = this.value.replace(/\.(?=.*\.)/g, '');
        }
    }
    
    /**
     * Shows error message for an input
     */
    function showError(inputElement, message) {
        removeError(inputElement);
        
        const errorMessage = document.createElement('div');
        errorMessage.className = 'invalid-feedback d-block';
        errorMessage.textContent = message;
        
        inputElement.classList.add('is-invalid');
        inputElement.parentNode.appendChild(errorMessage);
    }
    
    /**
     * Removes error message from an input
     */
    function removeError(inputElement) {
        inputElement.classList.remove('is-invalid');
        
        const errorMessage = inputElement.parentNode.querySelector('.invalid-feedback');
        if (errorMessage) {
            errorMessage.remove();
        }
    }
    
    /**
     * Shows or hides loading spinner in submit button
     */
    function showLoading(isLoading) {
        if (!submitButton || !buttonText || !loadingSpinner) return;
        
        if (isLoading) {
            buttonText.style.opacity = '0';
            loadingSpinner.classList.remove('d-none');
            submitButton.disabled = true;
        } else {
            buttonText.style.opacity = '1';
            loadingSpinner.classList.add('d-none');
            submitButton.disabled = false;
        }
    }
    
    /**
     * Animates elements in the results section with staggered timing
     */
    function animateResultsSection() {
        if (!resultsSection) return;
        
        // Animate breakdown cards with staggered delay
        const cards = resultsSection.querySelectorAll('.breakdown-card');
        cards.forEach((card, index) => {
            card.style.setProperty('--delay', index);
            card.classList.add('animate-in');
        });
    }

    // Set up dynamic input handlers
    function setupInputHandlers() {
        // Interest rate advice
        if (interestRate) {
            interestRate.addEventListener('input', function() {
                const rate = parseFloat(this.value);
                const helperText = this.closest('.form-group').querySelector('.helper-text');
                
                if (!helperText) return;
                
                if (rate < 7) {
                    updateHelperText(helperText, '💡 Excellent rate! This is below market average.', '#10b981');
                } else if (rate <= 9) {
                    updateHelperText(helperText, '💡 Good rate within normal range.', '#3b82f6');
                } else if (rate <= 12) {
                    updateHelperText(helperText, '💡 Consider negotiating for a better rate.', '#f59e0b');
                } else {
                    updateHelperText(helperText, '⚠️ This rate seems high. Shop around for better offers.', '#ef4444');
                }
            });
        }

        // Loan term advice
        if (loanTerm) {
            loanTerm.addEventListener('input', function() {
                const term = parseInt(this.value);
                const helperText = this.closest('.form-group').querySelector('.helper-text');
                
                if (!helperText) return;
                
                if (term <= 15) {
                    updateHelperText(helperText, '💡 Shorter term = Higher EMI but less total interest.', '#10b981');
                } else if (term <= 25) {
                    updateHelperText(helperText, '💡 Balanced choice between EMI and total interest.', '#3b82f6');
                } else {
                    updateHelperText(helperText, '💡 Longer term = Lower EMI but more total interest.', '#f59e0b');
                }
            });
        }

        // Live EMI preview
        if (loanAmount && interestRate && loanTerm && downPayment && buttonText) {
            [loanAmount, interestRate, loanTerm, downPayment].forEach(input => {
                input.addEventListener('input', debounce(calculatePreviewEMI, 300));
            });
        }
    }

    // Update helper text with formatting
    function updateHelperText(element, text, color) {
        element.innerHTML = text;
        element.style.color = color;
    }

    // Calculate preview EMI
    function calculatePreviewEMI() {
        const amount = parseFloat(loanAmount.value.replace(/,/g, '')) || 0;
        const downPaymentValue = parseFloat(downPayment.value.replace(/,/g, '')) || 0;
        const rate = parseFloat(interestRate.value) || 0;
        const tenure = parseFloat(loanTerm.value) || 0;

        if (amount && rate && tenure && amount > downPaymentValue) {
            const principal = amount - downPaymentValue;
            const monthlyRate = rate / (12 * 100);
            const numPayments = tenure * 12;
            
            try {
                const emi = (principal * monthlyRate * Math.pow(1 + monthlyRate, numPayments)) / 
                           (Math.pow(1 + monthlyRate, numPayments) - 1);
                
                if (!isNaN(emi) && emi > 0 && buttonText) {
                    buttonText.innerHTML = `<i class="fas fa-calculator me-2"></i>Calculate EMI (~₹${formatNumber(Math.round(emi))})`;
                }
            } catch (e) {
                console.error("EMI calculation error:", e);
                if (buttonText) {
                    buttonText.innerHTML = '<i class="fas fa-calculator me-2"></i>Calculate EMI';
                }
            }
        } else if (buttonText) {
            buttonText.innerHTML = '<i class="fas fa-calculator me-2"></i>Calculate EMI';
        }
    }

    // Format number with thousand separators
    function formatNumber(num) {
        return new Intl.NumberFormat('en-IN').format(num);
    }

    // Debounce function to limit expensive calculations
    function debounce(func, wait) {
        let timeout;
        return function() {
            const context = this;
            const args = arguments;
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(context, args), wait);
        };
    }
});
