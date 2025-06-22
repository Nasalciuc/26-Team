// Tinkerbell Frontend JavaScript - Lucian's Hour 1 & Hour 2 Work
// Handles page navigation, API calls, and data management

class TinkerbellApp {
    constructor() {
        this.currentPage = 'onboarding';
        this.businessData = {};
        this.personas = [];
        this.campaignData = {};
        this.uploadedImages = [];
        this.apiBaseUrl = 'http://localhost:3000/api';

        this.init();
    }
    init() {
            console.log('Tinkerbell App initialized');

            // Add global error handler
            window.addEventListener('error', (e) => {
                console.error('Global JavaScript Error:', e.error);
                console.error('Error message:', e.message);
                console.error('Error at:', e.filename + ':' + e.lineno);
            });

            window.addEventListener('unhandledrejection', (e) => {
                console.error('Unhandled Promise Rejection:', e.reason);
            });

            this.bindEvents();
            this.setupImageUpload();
            this.showPage('page-onboarding');
        } // Event Binding
    bindEvents() {
        console.log('Binding events...');

        // Page 1: Onboarding form submission
        const onboardingForm = document.getElementById('onboarding-form');
        if (onboardingForm) {
            console.log('Found onboarding form, adding event listener');
            onboardingForm.addEventListener('submit', (e) => {
                console.log('Form submit event triggered!');
                this.handleOnboardingSubmit(e);
            });
        } else {
            console.error('Onboarding form not found!');
        }

        // Page 2: Confirm personas button
        const confirmPersonasBtn = document.getElementById('confirm-personas');
        if (confirmPersonasBtn) {
            confirmPersonasBtn.addEventListener('click', () => this.handleConfirmPersonas());
        }

        // Page 3: Schedule campaign button
        const scheduleCampaignBtn = document.getElementById('schedule-campaign');
        if (scheduleCampaignBtn) {
            scheduleCampaignBtn.addEventListener('click', () => this.handleScheduleCampaign());
        }
    }

    // Setup image upload functionality
    setupImageUpload() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('image-upload');

        if (!uploadArea || !fileInput) return;

        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });

        // File input change
        fileInput.addEventListener('change', (e) => {
            this.handleFileSelection(e.target.files);
        });

        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            this.handleFileSelection(e.dataTransfer.files);
        });
    }

    // Handle file selection
    async handleFileSelection(files) {
        console.log('Files selected:', files.length);
        const validFiles = Array.from(files).filter(file => {
            const isImage = file.type.startsWith('image/');
            const isValidSize = file.size <= 10 * 1024 * 1024; // 10MB

            if (!isImage) {
                this.showError(`${file.name} is not a valid image`);
                return false;
            }
            if (!isValidSize) {
                this.showError(`${file.name} is too large (max 10MB)`);
                return false;
            }
            return true;
        });

        if (validFiles.length === 0) return;

        // Create image previews immediately
        validFiles.forEach(file => {
            this.createImagePreview(file);
        });

        // Upload files to server
        try {
            const formData = new FormData();
            validFiles.forEach(file => {
                formData.append('images', file);
            });

            const response = await fetch(`${this.apiBaseUrl}/upload-images`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error(`Upload failed: ${response.status}`);
            }

            const result = await response.json();
            console.log('Images uploaded:', result);

            // Store uploaded image data
            this.uploadedImages.push(...result.data.images);

            // Update preview with server data
            this.updateImagePreviews(result.data.images);
        } catch (error) {
            console.error('Upload failed:', error);
            this.showError('Error uploading images. Please try again.');
        }
    }

    // Create image preview
    createImagePreview(file) {
        const previewContainer = document.getElementById('uploaded-images-preview');
        if (!previewContainer) return;

        const preview = document.createElement('div');
        preview.className = 'image-preview';
        preview.dataset.fileName = file.name;

        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.alt = file.name;

        const info = document.createElement('div');
        info.className = 'image-info';
        info.textContent = `${file.name} (${this.formatFileSize(file.size)})`;

        const removeBtn = document.createElement('button');
        removeBtn.className = 'remove-image';
        removeBtn.innerHTML = '×';
        removeBtn.addEventListener('click', () => {
            this.removeImage(file.name, preview);
        });

        preview.appendChild(img);
        preview.appendChild(info);
        preview.appendChild(removeBtn);
        previewContainer.appendChild(preview);
    }

    // Update image previews with server data
    updateImagePreviews(serverImages) {
        serverImages.forEach(serverImage => {
            const preview = document.querySelector(`[data-file-name="${serverImage.originalName}"]`);
            if (preview) {
                // Update with server URL
                const img = preview.querySelector('img');
                img.src = `http://localhost:3000${serverImage.url}`;

                // Add server data
                preview.dataset.serverFilename = serverImage.filename;
                preview.dataset.serverPath = serverImage.path;
            }
        });
    }

    // Remove image
    removeImage(fileName, previewElement) {
        // Remove from uploaded images array
        this.uploadedImages = this.uploadedImages.filter(img => img.originalName !== fileName);

        // Remove preview element
        previewElement.remove();

        console.log(`🗑️ Removed image: ${fileName}`);
    }

    // Format file size
    formatFileSize(bytes) {
            if (bytes === 0) return '0 Bytes';
            const k = 1024;
            const sizes = ['Bytes', 'KB', 'MB', 'GB'];
            const i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
        } // Page Navigation
    showPage(pageId) {
            console.log(`Navigating to: ${pageId}`);

            // Hide all pages
            document.querySelectorAll('.page').forEach(page => {
                page.classList.remove('active');
            });

            // Show target page
            const targetPage = document.getElementById(pageId);
            if (targetPage) {
                targetPage.classList.add('active');
                this.currentPage = pageId.replace('page-', '');
            }

            // Page-specific actions
            if (pageId === 'page-personas') {
                this.showLoadingAnimation();
            }
        } // Loading Animation
    showLoadingAnimation() {
            const loadingSection = document.getElementById('loading-log');
            const personasEditor = document.getElementById('personas-editor');

            if (loadingSection && personasEditor) {
                loadingSection.style.display = 'block';
                personasEditor.style.display = 'none';

                // Show editor after animation
                setTimeout(() => {
                    loadingSection.style.display = 'none';
                    personasEditor.style.display = 'block';
                }, 3000);
            }
        } // Page 1: Handle onboarding form submission
    async handleOnboardingSubmit(e) {
        console.log('🚀 handleOnboardingSubmit called!');
        e.preventDefault();
        console.log('📋 Form default prevented, processing onboarding form...');

        const formData = new FormData(e.target);
        this.businessData = {
            businessName: formData.get('businessName'),
            businessDescription: formData.get('businessDescription'),
            targetCustomers: formData.get('targetCustomers'),
            goals: formData.get('businessGoals'),
            websiteUrl: formData.get('websiteUrl')
        };

        console.log('🏪 Business data collected:', this.businessData); // Validate required fields
        if (!this.businessData.businessName || !this.businessData.businessDescription) {
            console.error('Missing required fields');
            this.showError('Please fill in all required fields.');
            return;
        }

        console.log('✅ Validation passed, making API call...');

        try {
            // Show loading page first
            this.showPage('page-personas');

            console.log('🌐 Making API call to:', `${this.apiBaseUrl}/create-personas`);
            console.log('📤 Request data:', JSON.stringify(this.businessData));

            // Call create-personas API (Vladimir's endpoint)
            const response = await fetch(`${this.apiBaseUrl}/create-personas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.businessData)
            });

            console.log('📡 Response received:', response.status, response.statusText);

            if (!response.ok) {
                const errorText = await response.text();
                console.error('❌ API Error response:', errorText);
                throw new Error(`API Error: ${response.status} - ${response.statusText}`);
            }

            const result = await response.json();
            console.log('🧠 Personas received:', result);

            if (result.success && result.data && result.data.personas) {
                this.personas = result.data.personas;
                this.populatePersonasEditor();
                console.log('✅ Personas populated successfully');
            } else {
                throw new Error('Invalid personas response format');
            }

        } catch (error) {
            console.error('❌ Error generating personas:', error);
            console.error('❌ Error details:', error.stack); // Go back to onboarding page on error
            this.showPage('page-onboarding');
            this.showError(`An error occurred while generating personas: ${error.message}`);
        }
    }

    // Populate personas editor with received data
    populatePersonasEditor() {
        const container = document.getElementById('personas-container');
        if (!container) return;

        console.log('Populating personas editor...');
        container.innerHTML = '';

        this.personas.forEach((persona, index) => {
            const personaCard = this.createPersonaCard(persona, index);
            container.appendChild(personaCard);
        });
    }

    // Create editable persona card
    createPersonaCard(persona, index) {
            const card = document.createElement('div');
            card.className = 'persona-card';
            card.innerHTML = `
            <div class="persona-header">
                <div class="persona-avatar">${index + 1}</div>
                <div class="persona-info">
                    <h4>${persona.name}</h4>
                    <p>${persona.age_range}</p>
                </div>
            </div>
            
            <div class="persona-details">
                <p><strong>Demographics:</strong> ${persona.demographics}</p>
                <p><strong>Interests:</strong> ${Array.isArray(persona.interests) ? persona.interests.join(', ') : persona.interests}</p>
                <p><strong>Pain points:</strong> ${Array.isArray(persona.pain_points) ? persona.pain_points.join(', ') : persona.pain_points}</p>
                <p><strong>Communication style:</strong> ${persona.communication_style}</p>
            </div>
            
            <div class="persona-edit">
                <h5>Edit persona:</h5>
                <textarea name="persona_edit_${index}" placeholder="Make any changes to this persona...">${persona.demographics}</textarea>
            </div>
        `;

            return card;
        } // Page 2: Handle personas confirmation
    async handleConfirmPersonas() {
            console.log('✅ Confirming personas...');

            // Collect edited persona data
            const editedPersonas = this.collectEditedPersonas();
            console.log('📝 Edited personas:', editedPersonas);

            // Check if we should generate missing images
            const generateMissingImagesEl = document.getElementById('generate-missing-images');
            const generateMissingImages = generateMissingImagesEl ? generateMissingImagesEl.checked : true;

            try {
                // Show campaign page
                this.showPage('page-campaign');

                // Prepare form data for enhanced campaign with images
                const formData = new FormData();
                formData.append('businessData', JSON.stringify(this.businessData));
                formData.append('confirmedPersonas', JSON.stringify(editedPersonas));
                formData.append('generateMissingImages', generateMissingImages);

                // Add uploaded images to form data
                if (this.uploadedImages && this.uploadedImages.length > 0) {
                    console.log(`📷 Including ${this.uploadedImages.length} uploaded images`);
                    // Note: Images are already uploaded to server, we'll reference them by server data
                    formData.append('uploadedImageData', JSON.stringify(this.uploadedImages));
                }

                // Call enhanced schedule-campaign-with-images API
                const response = await fetch(`${this.apiBaseUrl}/schedule-campaign-with-images`, {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error(`API Error: ${response.status}`);
                }

                const result = await response.json();
                console.log('🚀 Enhanced campaign result:', result);

                if (result.success && result.data) {
                    this.campaignData = result.data;
                    this.populateCampaignDashboard();

                    // Show image processing results if available
                    if (result.data.images) {
                        this.displayImageProcessingResults(result.data.images);
                    }

                    // Show auto-posting status if enabled
                    if (result.data.auto_posting && result.data.auto_posting.enabled) {
                        this.displayAutoPostingStatus(result.data.auto_posting);
                    }
                } else {
                    throw new Error('Invalid campaign response');
                }
            } catch (error) {
                console.error('Error generating enhanced campaign:', error);
                this.showError('An error occurred while generating the campaign. Please try again.');
            }
        } // Collect edited persona data from form
    collectEditedPersonas() {
        const editedPersonas = [];
        const container = document.getElementById('personas-container');
        const personaCards = container.querySelectorAll('.persona-card');

        personaCards.forEach((card, index) => {
            const editText = card.querySelector(`textarea[name="persona_edit_${index}"]`).value;
            const originalPersona = this.personas[index];

            const persona = {
                ...originalPersona,
                demographics: editText || originalPersona.demographics
            };
            editedPersonas.push(persona);
        });

        return editedPersonas;
    }

    // Populate campaign dashboard
    populateCampaignDashboard() {
            console.log('📊 Populating campaign dashboard...');

            // Set strategy
            const strategyElement = document.getElementById('marketing-strategy');
            if (strategyElement && this.campaignData.campaign && this.campaignData.campaign.strategy) {
                strategyElement.textContent = this.campaignData.campaign.strategy;
            }

            // Populate posts
            const postsContainer = document.getElementById('posts-container');
            if (postsContainer && this.campaignData.campaign && this.campaignData.campaign.posts) {
                postsContainer.innerHTML = '';

                this.campaignData.campaign.posts.forEach((post, index) => {
                    const postCard = this.createPostCard(post, index);
                    postsContainer.appendChild(postCard);
                });
            }
        } // Create post card for display
    createPostCard(post, index) {
        const card = document.createElement('div');
        card.className = 'post-card';

        const platformClass = `platform-${post.platform}`;
        const platformText = post.platform === 'both' ? 'Facebook & Instagram' :
            post.platform === 'facebook' ? 'Facebook' : 'Instagram';

        // Check for image data
        let imageHTML = '';
        if (post.image) {
            const imageUrl = post.image.url || post.image.imageUrl ||
                (post.image.filename ? `http://localhost:3000/images/${post.image.filename}` : null);
            if (imageUrl) {
                imageHTML = `
                    <div class="post-image-preview">
                        <img src="${imageUrl}" alt="Post image" onerror="this.style.display='none'">
                        <div class="image-source-badge ${post.image.source || 'unknown'}">${post.image.source || 'image'}</div>
                    </div>
                `;
                card.classList.add('with-image');
            }
        }

        card.innerHTML = `
            <div class="post-header">
                <span class="platform-badge ${platformClass}">${platformText}</span>
                <span class="post-goal">${post.post_goal}</span>
            </div>
            
            <div class="post-content">
                <div class="post-text">${post.post_text}</div>
                <div class="post-hashtags">${Array.isArray(post.hashtags) ? post.hashtags.join(' ') : post.hashtags}</div>
                <div class="post-cta">📞 ${post.call_to_action}</div>
            </div>
            
            ${imageHTML}
            
            <div class="post-meta">
                <small>🎯 Țintește: ${post.target_persona}</small><br>
                <small>🖼️ ${post.image_description}</small>
            </div>
        `;

        return card;
    }

    // Page 3: Handle campaign scheduling
    handleScheduleCampaign() {
        console.log('🎉 Launching campaign...');

        // Show success page with campaign details
        this.showSuccessPage();
    }

    // Show success page with results
    showSuccessPage() {
        this.showPage('page-success');

        // Update success details
        if (this.campaignData.scheduling) {
            const postsCount = document.getElementById('posts-count');
            if (postsCount) {
                postsCount.textContent = this.campaignData.scheduling.successful;
            }
        }

        // Set workspace link
        const workspaceLink = document.getElementById('workspace-link');
        if (workspaceLink && this.campaignData.workspace) {
            workspaceLink.href = this.campaignData.workspace.url;
            workspaceLink.textContent = `🚀 ${this.campaignData.workspace.name}`;
        }

        // Update success details list
        const successDetails = document.getElementById('success-details');
        if (successDetails && this.campaignData) {
            successDetails.innerHTML = `
                <li>✨ Workspace "${this.campaignData.workspace?.name || 'Tinkerbell Campaign'}" creat în Planable</li>
                <li>📱 ${this.campaignData.scheduling?.successful || 3} postări programate cu succes</li>
                <li>🎯 Campania gata de lansare și monitorizare</li>
                <li>💡 Strategia: ${this.campaignData.campaign?.strategy || 'Strategie personalizată generată'}</li>
            `;
        }

        // Celebration animation
        this.triggerCelebration();
    }

    // Trigger celebration animation
    triggerCelebration() {
            console.log('🎉 Triggering celebration!');

            // You could add confetti or other celebration effects here
            const animation = document.querySelector('.success-animation');
            if (animation) {
                animation.style.animation = 'bounce 1s ease-in-out 3';
            }
        } // Error handling
    showError(message) {
        console.error('Showing error:', message);
        alert(`Error: ${message}`);

        // Don't auto-reload anymore - let the user decide what to do
        // The calling function should handle navigation appropriately
    }

    // Utility: Log current state
    logState() {
            console.log('📊 Current app state:', {
                currentPage: this.currentPage,
                businessData: this.businessData,
                personas: this.personas,
                campaignData: this.campaignData
            });
        } // Display image processing results
    displayImageProcessingResults(imageData) {
            console.log('🖼️ Displaying image processing results:', imageData);

            const resultsContainer = document.getElementById('image-processing-results');
            if (!resultsContainer) return;

            let resultsHTML = '<div class="image-results-section">';
            resultsHTML += '<h3>📸 Rezultate procesare imagini</h3>';

            if (imageData.processing_summary) {
                const summary = imageData.processing_summary;
                resultsHTML += `
                <div class="processing-summary">
                    <p><strong>Postări totale:</strong> ${summary.total_posts}</p>
                    <p><strong>Postări cu imagini:</strong> ${summary.posts_with_images}</p>
                    <p><strong>Imagini încărcate asociate:</strong> ${summary.matched_images}</p>
                    <p><strong>Imagini generate:</strong> ${summary.generated_images}</p>
                </div>
            `;
            } else {
                // Fallback display when no processing summary available
                const uploadedCount = this.uploadedImages ? this.uploadedImages.length : 0;
                resultsHTML += `
                <div class="processing-summary">
                    <p><strong>Imagini încărcate:</strong> ${uploadedCount}</p>
                    <p><strong>Status:</strong> ${uploadedCount > 0 ? 'Imagini procesate cu succes' : 'Nu au fost încărcate imagini'}</p>
                </div>
            `;
            }

            if (imageData.matched_images && imageData.matched_images.length > 0) {
                resultsHTML += '<h4>✅ Imagini asociate automat:</h4>';
                imageData.matched_images.forEach(match => {
                    resultsHTML += `
                    <div class="matched-image-result">
                        <p><strong>${match.image.filename}</strong> → ${match.post.platform} post (${match.confidence}% potrivire)</p>
                    </div>
                `;
                });
            }

            if (imageData.generated_images && imageData.generated_images.length > 0) {
                resultsHTML += '<h4>🎨 Imagini generate:</h4>';
                imageData.generated_images.forEach(img => {
                            resultsHTML += `
                    <div class="generated-image-result">
                        <p><strong>Generată:</strong> ${img.description}</p>
                        ${img.url ? `<img src="${img.url}" alt="Generated image" style="max-width: 200px; border-radius: 8px; margin-top: 8px;">` : ''}
                    </div>
                `;
            });
        }

        resultsHTML += '</div>';
        resultsContainer.innerHTML = resultsHTML;
        resultsContainer.style.display = 'block';
    }

    // Display auto-posting status
    displayAutoPostingStatus(autoPostingData) {
        console.log('🚀 Displaying auto-posting status:', autoPostingData);

        const statusContainer = document.getElementById('auto-posting-status');
        if (!statusContainer) return;

        let statusHTML = '<div class="auto-posting-section">';
        statusHTML += '<h3>🎯 Status Auto-Postare</h3>';

        if (autoPostingData.enabled) {
            statusHTML += `
                <div class="auto-posting-enabled">
                    <p>✅ <strong>Auto-postarea este activă!</strong></p>
                    <p>📘 Facebook Page ID: ${autoPostingData.facebook_page_id}</p>
                    <p>🚀 Postările vor fi publicate automat pe Facebook prin Planable</p>
                </div>
            `;
        } else {
            statusHTML += `
                <div class="auto-posting-disabled">
                    <p>⏸️ Auto-postarea este dezactivată</p>
                    <p>Postările vor fi create ca draft-uri în Planable pentru revizuire manuală</p>
                </div>
            `;
        }

        statusHTML += '</div>';
        statusContainer.innerHTML = statusHTML;
        statusContainer.style.display = 'block';
    }
}

// Initialize app when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 DOM loaded, initializing Tinkerbell...');
    window.tinkerbellApp = new TinkerbellApp();
});

// Utility functions for debugging
window.debugTinkerbell = () => {
    if (window.tinkerbellApp) {
        window.tinkerbellApp.logState();
    }
};

// Handle page refresh warning
window.addEventListener('beforeunload', (e) => {
    if (window.tinkerbellApp && window.tinkerbellApp.currentPage !== 'onboarding') {
        e.preventDefault();
        e.returnValue = 'Are you sure you want to leave this page? Your progress will be lost.';
    }
});