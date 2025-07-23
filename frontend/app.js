// Pub Quiz Frontend Application
const API_BASE_URL = 'http://localhost:8000';

// DOM Elements
const questionForm = document.getElementById('question-form');
const categorySelect = document.getElementById('category');
const subcategorySelect = document.getElementById('subcategory');
const questionTypeSelect = document.getElementById('question_type');
const mediaUploadSection = document.getElementById('media-upload-section');
const fileInput = document.getElementById('media_file');
const filePreview = document.getElementById('file-preview');
const fileName = document.getElementById('file-name');
const removeFileBtn = document.getElementById('remove-file');
const fileTypes = document.getElementById('file-types');
const submitButton = document.getElementById('submit-button');
const submitText = document.getElementById('submit-text');
const submitLoading = document.getElementById('submit-loading');
const messageContainer = document.getElementById('message-container');
const successMessage = document.getElementById('success-message');
const errorMessage = document.getElementById('error-message');
const successText = document.getElementById('success-text');
const errorText = document.getElementById('error-text');
const statusIndicator = document.getElementById('status-indicator');
const statusText = document.getElementById('status-text');

// Global variables
let categories = {};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    checkApiConnection();
    loadCategories();
    setupEventListeners();
});

// Check API connection status
async function checkApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            updateStatus('connected', 'API Connected');
        } else {
            updateStatus('error', 'API Error');
        }
    } catch (error) {
        updateStatus('error', 'API Disconnected');
    }
}

// Update connection status indicator
function updateStatus(status, message) {
    statusText.textContent = message;
    statusIndicator.className = 'w-2 h-2 rounded-full';
    
    switch (status) {
        case 'connected':
            statusIndicator.classList.add('bg-quiz-green');
            break;
        case 'error':
            statusIndicator.classList.add('bg-quiz-red');
            break;
        default:
            statusIndicator.classList.add('bg-gray-400');
    }
}

// Load categories from API
async function loadCategories() {
    try {
        const response = await fetch(`${API_BASE_URL}/categories`);
        if (!response.ok) {
            throw new Error('Failed to fetch categories');
        }
        
        categories = await response.json();
        populateCategoryDropdown();
        
    } catch (error) {
        console.error('Error loading categories:', error);
        showError('Failed to load categories. Please refresh the page.');
        categorySelect.innerHTML = '<option value="">Error loading categories</option>';
    }
}

// Populate category dropdown
function populateCategoryDropdown() {
    categorySelect.innerHTML = '<option value="">Select a category...</option>';
    
    Object.keys(categories).forEach(category => {
        const option = document.createElement('option');
        option.value = category;
        option.textContent = category;
        categorySelect.appendChild(option);
    });
}

// Update subcategory dropdown based on selected category
function updateSubcategories() {
    const selectedCategory = categorySelect.value;
    subcategorySelect.innerHTML = '<option value="">Select a subcategory...</option>';
    
    if (selectedCategory && categories[selectedCategory]) {
        subcategorySelect.disabled = false;
        
        categories[selectedCategory].forEach(subcategory => {
            const option = document.createElement('option');
            option.value = subcategory;
            option.textContent = subcategory;
            subcategorySelect.appendChild(option);
        });
    } else {
        subcategorySelect.disabled = true;
        subcategorySelect.innerHTML = '<option value="">Select a category first...</option>';
    }
}

// Show/hide media upload based on question type
function updateMediaUpload() {
    const questionType = questionTypeSelect.value;
    const mediaTypes = ['image', 'video', 'audio'];
    
    if (mediaTypes.includes(questionType)) {
        mediaUploadSection.classList.remove('hidden');
        
        // Update file input accept attribute and help text
        switch (questionType) {
            case 'image':
                fileInput.accept = 'image/*';
                fileTypes.textContent = 'PNG, JPG, GIF up to 10MB';
                break;
            case 'video':
                fileInput.accept = 'video/*';
                fileTypes.textContent = 'MP4, WebM, AVI up to 10MB';
                break;
            case 'audio':
                fileInput.accept = 'audio/*';
                fileTypes.textContent = 'MP3, WAV, OGG up to 10MB';
                break;
        }
    } else {
        mediaUploadSection.classList.add('hidden');
        clearFileSelection();
    }
}

// Handle file selection
function handleFileSelect(event) {
    const file = event.target.files[0];
    
    if (file) {
        // Check file size (10MB limit)
        const maxSize = 10 * 1024 * 1024; // 10MB in bytes
        if (file.size > maxSize) {
            showError('File size must be less than 10MB');
            clearFileSelection();
            return;
        }
        
        fileName.textContent = file.name;
        filePreview.classList.remove('hidden');
    }
}

// Clear file selection
function clearFileSelection() {
    fileInput.value = '';
    filePreview.classList.add('hidden');
    fileName.textContent = '';
}

// Setup event listeners
function setupEventListeners() {
    // Category change
    categorySelect.addEventListener('change', updateSubcategories);
    
    // Question type change
    questionTypeSelect.addEventListener('change', updateMediaUpload);
    
    // File selection
    fileInput.addEventListener('change', handleFileSelect);
    
    // Remove file
    removeFileBtn.addEventListener('click', clearFileSelection);
    
    // Form submission
    questionForm.addEventListener('submit', handleFormSubmit);
}

// Handle form submission
async function handleFormSubmit(event) {
    event.preventDefault();
    
    const formData = new FormData(questionForm);
    const questionData = {
        question_text: formData.get('question_text'),
        answer_text: formData.get('answer_text'),
        question_type: formData.get('question_type'),
        category: formData.get('category'),
        subcategory: formData.get('subcategory')
    };
    
    // Add media file path if file is selected
    if (fileInput.files[0]) {
        // For now, we'll just store the filename
        // In a real implementation, you'd upload the file first
        questionData.media_file_path = `media/${questionData.question_type}s/${fileInput.files[0].name}`;
    }
    
    try {
        setLoading(true);
        hideMessages();
        
        const response = await fetch(`${API_BASE_URL}/questions/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(questionData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || 'Failed to create question');
        }
        
        const result = await response.json();
        showSuccess(`Question created successfully! ID: ${result.id}`);
        resetForm();
        
    } catch (error) {
        console.error('Error creating question:', error);
        showError(error.message || 'Failed to create question. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Set loading state
function setLoading(loading) {
    submitButton.disabled = loading;
    submitText.classList.toggle('hidden', loading);
    submitLoading.classList.toggle('hidden', !loading);
}

// Show success message
function showSuccess(message) {
    successText.textContent = message;
    successMessage.classList.remove('hidden');
    errorMessage.classList.add('hidden');
    messageContainer.classList.remove('hidden');
    
    // Scroll to top to show message
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Show error message
function showError(message) {
    errorText.textContent = message;
    errorMessage.classList.remove('hidden');
    successMessage.classList.add('hidden');
    messageContainer.classList.remove('hidden');
    
    // Scroll to top to show message
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Hide all messages
function hideMessages() {
    messageContainer.classList.add('hidden');
    successMessage.classList.add('hidden');
    errorMessage.classList.add('hidden');
}

// Reset form after successful submission
function resetForm() {
    questionForm.reset();
    subcategorySelect.disabled = true;
    subcategorySelect.innerHTML = '<option value="">Select a category first...</option>';
    mediaUploadSection.classList.add('hidden');
    clearFileSelection();
}

// Utility function to validate form
function validateForm() {
    const requiredFields = ['question_text', 'answer_text', 'question_type', 'category', 'subcategory'];
    
    for (const field of requiredFields) {
        const value = questionForm.elements[field].value.trim();
        if (!value) {
            showError(`Please fill in the ${field.replace('_', ' ')} field.`);
            return false;
        }
    }
    
    return true;
}

// Auto-save functionality (optional enhancement)
function autoSave() {
    const formData = {
        question_text: document.getElementById('question_text').value,
        answer_text: document.getElementById('answer_text').value,
        question_type: questionTypeSelect.value,
        category: categorySelect.value,
        subcategory: subcategorySelect.value
    };
    
    localStorage.setItem('quiz_form_draft', JSON.stringify(formData));
}

// Restore auto-saved data (optional enhancement)
function restoreAutoSave() {
    const saved = localStorage.getItem('quiz_form_draft');
    if (saved) {
        try {
            const data = JSON.parse(saved);
            document.getElementById('question_text').value = data.question_text || '';
            document.getElementById('answer_text').value = data.answer_text || '';
            questionTypeSelect.value = data.question_type || '';
            categorySelect.value = data.category || '';
            
            if (data.category) {
                updateSubcategories();
                setTimeout(() => {
                    subcategorySelect.value = data.subcategory || '';
                }, 100);
            }
            
            updateMediaUpload();
        } catch (error) {
            console.error('Error restoring auto-save:', error);
        }
    }
}

// Clear auto-save after successful submission
function clearAutoSave() {
    localStorage.removeItem('quiz_form_draft');
}

// Add auto-save listeners (optional enhancement)
document.addEventListener('DOMContentLoaded', function() {
    // Restore any auto-saved data
    setTimeout(restoreAutoSave, 500);
    
    // Auto-save on input changes
    const inputs = questionForm.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', autoSave);
        input.addEventListener('change', autoSave);
    });
});

// Check API connection periodically
setInterval(checkApiConnection, 30000); // Check every 30 seconds 