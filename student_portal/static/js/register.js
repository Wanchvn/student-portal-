/**
 * Registration page - form validation and dynamic select loading
 */

const EMAIL_REGEX = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
const PHONE_REGEX = /^\+?[\d\s\-()]{7,20}$/;
const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png'];
const ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png'];

document.addEventListener('DOMContentLoaded', () => {
    loadDepartments();
    loadProgrammes();
    setupImagePreview();
    setupFormValidation();
});

/**
 * Fetch departments from API and populate select box
 */
async function loadDepartments() {
    const select = document.getElementById('department');
    if (!select) return;

    try {
        const response = await fetch('/api/departments');
        if (!response.ok) throw new Error('Failed to load departments');

        const departments = await response.json();
        select.innerHTML = '<option value="">Select Department</option>';

        departments.forEach((dept) => {
            const option = document.createElement('option');
            option.value = dept.name;
            option.textContent = dept.name;
            select.appendChild(option);
        });
    } catch (error) {
        select.innerHTML = '<option value="">Error loading departments</option>';
        console.error('Department load error:', error);
    }
}

/**
 * Fetch programmes from API and populate select box
 */
async function loadProgrammes() {
    const select = document.getElementById('programme');
    if (!select) return;

    try {
        const response = await fetch('/api/programmes');
        if (!response.ok) throw new Error('Failed to load programmes');

        const programmes = await response.json();
        select.innerHTML = '<option value="">Select Programme</option>';

        programmes.forEach((prog) => {
            const option = document.createElement('option');
            option.value = prog.name;
            option.textContent = prog.name;
            select.appendChild(option);
        });
    } catch (error) {
        select.innerHTML = '<option value="">Error loading programmes</option>';
        console.error('Programme load error:', error);
    }
}

/**
 * Show image preview when file is selected
 */
function setupImagePreview() {
    const imageInput = document.getElementById('image');
    const previewContainer = document.getElementById('imagePreview');
    const previewImg = previewContainer?.querySelector('img');

    if (!imageInput || !previewContainer || !previewImg) return;

    imageInput.addEventListener('change', () => {
        const file = imageInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                previewImg.src = e.target.result;
                previewContainer.classList.remove('d-none');
            };
            reader.readAsDataURL(file);
        } else {
            previewContainer.classList.add('d-none');
        }
    });
}

/**
 * Display validation error beside a field
 */
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(`error-${fieldId}`);

    if (field) {
        field.classList.add('is-invalid');
    }
    if (errorEl) {
        errorEl.textContent = message;
    }
}

/**
 * Clear validation error for a field
 */
function clearError(fieldId) {
    const field = document.getElementById(fieldId);
    const errorEl = document.getElementById(`error-${fieldId}`);

    if (field) {
        field.classList.remove('is-invalid');
    }
    if (errorEl) {
        errorEl.textContent = '';
    }
}

/**
 * Validate all form fields
 */
function validateForm() {
    let isValid = true;
    const fields = [
        'full_name', 'address', 'email', 'phone', 'date_of_birth',
        'department', 'programme'
    ];

    fields.forEach(clearError);
    clearError('gender');
    clearError('image');

    const fullName = document.getElementById('full_name').value.trim();
    if (!fullName) {
        showError('full_name', 'Full name is required.');
        isValid = false;
    }

    const address = document.getElementById('address').value.trim();
    if (!address) {
        showError('address', 'Address is required.');
        isValid = false;
    }

    const email = document.getElementById('email').value.trim();
    if (!email) {
        showError('email', 'Email is required.');
        isValid = false;
    } else if (!EMAIL_REGEX.test(email)) {
        showError('email', 'Please enter a valid email address.');
        isValid = false;
    }

    const phone = document.getElementById('phone').value.trim();
    if (!phone) {
        showError('phone', 'Phone number is required.');
        isValid = false;
    } else if (!PHONE_REGEX.test(phone)) {
        showError('phone', 'Please enter a valid phone number.');
        isValid = false;
    }

    const dob = document.getElementById('date_of_birth').value;
    if (!dob) {
        showError('date_of_birth', 'Date of birth is required.');
        isValid = false;
    }

    const gender = document.querySelector('input[name="gender"]:checked');
    if (!gender) {
        showError('gender', 'Please select a gender.');
        isValid = false;
    }

    const department = document.getElementById('department').value;
    if (!department) {
        showError('department', 'Please select a department.');
        isValid = false;
    }

    const programme = document.getElementById('programme').value;
    if (!programme) {
        showError('programme', 'Please select a programme.');
        isValid = false;
    }

    const imageInput = document.getElementById('image');
    const file = imageInput.files[0];
    if (!file) {
        showError('image', 'Profile image is required.');
        isValid = false;
    } else {
        const ext = file.name.split('.').pop().toLowerCase();
        if (!ALLOWED_EXTENSIONS.includes(ext) || !ALLOWED_IMAGE_TYPES.includes(file.type)) {
            showError('image', 'Only JPG, JPEG, and PNG images are allowed.');
            isValid = false;
        }
    }

    return isValid;
}

/**
 * Attach form submit validation
 */
function setupFormValidation() {
    const form = document.getElementById('registrationForm');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        if (!validateForm()) {
            e.preventDefault();
        }
    });
}
