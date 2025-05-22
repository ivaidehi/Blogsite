// Image preview functionality
function previewImage(event) {
    const preview = document.getElementById("profilePreview");
    const placeholder = document.getElementById("profilePlaceholder");
    const file = event.target.files[0];
    
    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = "block";
        placeholder.style.display = "none";
    } else {
        preview.style.display = "none";
        placeholder.style.display = "flex";
    }
}

// Toggle password visibility
function togglePassword(inputId, button) {
    const input = document.getElementById(inputId);
    const icon = button.querySelector('i');
    
    if (input.type === "password") {
        input.type = "text";
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    } else {
        input.type = "password";
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }
    
    // Apply a subtle animation
    button.style.transform = "scale(1.1)";
    setTimeout(() => {
        button.style.transform = "scale(1)";
    }, 200);
}

// Password strength indicator
document.getElementById("id_password1").addEventListener("input", function () {
    const password = this.value;
    const warning = document.getElementById("passwordWarning");

    let message = "";
    if (password.length === 0) {
        message = "";
    } else if (password.length < 8) {
        message = "Password must be at least 8 characters";
    } else if (!/[A-Z]/.test(password)) {
        message = "Include at least one uppercase letter";
    } else if (!/[0-9]/.test(password)) {
        message = "Include at least one number";
    } else if (!/[^A-Za-z0-9]/.test(password)) {
        message = "Include at least one special character";
    } else {
        message = ""; // Password is strong enough
    }

    warning.textContent = message;
});


// Check password match
function checkPasswordMatch() {
    const password1 = document.getElementById("id_password1").value;
    const password2 = document.getElementById("id_password2").value;
    const mismatchElement = document.getElementById("passwordMismatch");
    
    if (password1 && password2) {
        if (password1 !== password2) {
            mismatchElement.style.display = "block";
            document.getElementById("id_password2").classList.add("error-border");
        } else {
            mismatchElement.style.display = "none";
            document.getElementById("id_password2").classList.remove("error-border");
        }
    } else {
        mismatchElement.style.display = "none";
        document.getElementById("id_password2").classList.remove("error-border");
    }
}

document.getElementById("id_password2").addEventListener("input", checkPasswordMatch);

// Username availability check
document.getElementById("id_username").addEventListener("blur", function() {
    const username = this.value;
    
    if (username) {
        // Add loading indicator
        const loadingElement = document.createElement("div");
        loadingElement.className = "loading-indicator";
        loadingElement.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Checking availability...';
        loadingElement.style.color = "var(--medium-gray)";
        loadingElement.style.fontSize = "0.8rem";
        loadingElement.style.marginTop = "0.25rem";
        
        const parent = this.parentElement;
        const existingLoading = parent.querySelector(".loading-indicator");
        const existingError = parent.querySelector(".username-error");
        
        if (existingLoading) parent.removeChild(existingLoading);
        if (existingError) parent.removeChild(existingError);
        
        parent.appendChild(loadingElement);
        
        // Check username availability
        fetch(`/check_username/?username=${username}`)
            .then(response => response.json())
            .then(data => {
                parent.removeChild(loadingElement);
                
                if (data.exists) {
                    const errorElement = document.createElement("div");
                    errorElement.className = "error username-error";
                    errorElement.innerHTML = '<i class="fas fa-exclamation-circle"></i> This username is not available';
                    parent.appendChild(errorElement);
                    this.classList.add("error-border");
                } else {
                    const successElement = document.createElement("div");
                    successElement.className = "strength-indicator strong username-error";
                    successElement.innerHTML = '<i class="fas fa-check-circle"></i> Username is available';
                    parent.appendChild(successElement);
                    this.classList.remove("error-border");
                }
            })
            .catch(() => {
                parent.removeChild(loadingElement);
            });
    }
});

// Simple form validation
document.getElementById("signupForm").addEventListener("submit", function(e) {
    const password1 = document.getElementById("id_password1").value;
    const password2 = document.getElementById("id_password2").value;
    
    if (password1 !== password2) {
        e.preventDefault();
        document.getElementById("passwordMismatch").style.display = "block";
        document.getElementById("id_password2").classList.add("error-border");
        
        // Scroll to password field
        document.getElementById("id_password2").scrollIntoView({
            behavior: "smooth",
            block: "center"
        });
    }
});

// Add subtle animation to form inputs
const inputs = document.querySelectorAll("input");
inputs.forEach(input => {
    input.addEventListener("focus", function() {
        this.parentElement.style.transform = "translateY(-2px)";
        this.parentElement.style.transition = "transform 0.3s ease";
    });
    
    input.addEventListener("blur", function() {
        this.parentElement.style.transform = "translateY(0)";
    });
});

// Add this to script.js after the existing code

// Field validation on blur
function validateField(field, fieldName) {
    const value = field.value.trim();
    const parent = field.parentElement;
    let errorElement = parent.querySelector('.field-error');
    
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'error field-error';
        parent.appendChild(errorElement);
    }
    
    if (field.required && !value) {
        errorElement.textContent = `${fieldName} is required`;
        field.classList.add('error-border');
        return false;
    }
    
    // Additional validations for specific fields
    if (field.id === 'id_email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            errorElement.textContent = 'Please enter a valid email address';
            field.classList.add('error-border');
            return false;
        }
    }
    
    if (field.id === 'id_pincode' && value) {
        const pincodeRegex = /^\d{6}$/;
        if (!pincodeRegex.test(value)) {
            errorElement.textContent = 'Pincode must be 6 digits';
            field.classList.add('error-border');
            return false;
        }
    }
    
    // Clear error if valid
    errorElement.textContent = '';
    field.classList.remove('error-border');
    return true;
}

// Add blur event listeners to all required fields
document.querySelectorAll('input[required], select[required]').forEach(field => {
    field.addEventListener('blur', function() {
        const fieldName = this.labels[0].textContent.replace(' *', '');
        validateField(this, fieldName);
    });
});

// Form submission validation
document.getElementById('signupForm').addEventListener('submit', function(e) {
    let isValid = true;
    const requiredFields = document.querySelectorAll('input[required], select[required]');
    
    requiredFields.forEach(field => {
        const fieldName = field.labels[0].textContent.replace(' *', '');
        if (!validateField(field, fieldName)) {
            isValid = false;
        }
    });
    
    // Password match validation
    const password1 = document.getElementById('id_password1').value;
    const password2 = document.getElementById('id_password2').value;
    if (password1 !== password2) {
        document.getElementById('passwordMismatch').style.display = 'block';
        document.getElementById('id_password2').classList.add('error-border');
        isValid = false;
        
        // Scroll to password field
        document.getElementById('id_password2').scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
    }
    
    if (!isValid) {
        e.preventDefault();
        
        // Scroll to first error
        const firstError = document.querySelector('.error-border');
        if (firstError) {
            firstError.scrollIntoView({
                behavior: 'smooth',
                block: 'center'
            });
        }
    }
});