// Tinkerbell Frontend JavaScript - Lucian's Hour 1 & Hour 2 Work
// Handles page navigation, API calls, and data management

class TinkerbellApp {
    constructor() {
        this.currentPage = 'onboarding';
        this.businessData = {};
        this.personas = [];
        this.campaignData = {};
        this.apiBaseUrl = 'http://localhost:3000/api';

        this.init();
    }

    init() {
        console.log('🎯 Tinkerbell App initialized');
        this.bindEvents();
        this.showPage('page-onboarding');
    }

    // Event Binding
    bindEvents() {
        // Page 1: Onboarding form submission
        const onboardingForm = document.getElementById('onboarding-form');
        if (onboardingForm) {
            onboardingForm.addEventListener('submit', (e) => this.handleOnboardingSubmit(e));
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

    // Page Navigation
    showPage(pageId) {
        console.log(`📄 Navigating to: ${pageId}`);

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
    }

    // Loading Animation
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
    }

    // Page 1: Handle onboarding form submission
    async handleOnboardingSubmit(e) {
        e.preventDefault();
        console.log('📋 Processing onboarding form...');

        const formData = new FormData(e.target);
        this.businessData = {
            businessName: formData.get('businessName'),
            businessDescription: formData.get('businessDescription'),
            targetCustomers: formData.get('targetCustomers'),
            goals: formData.get('businessGoals'),
            websiteUrl: formData.get('websiteUrl')
        };

        console.log('🏪 Business data collected:', this.businessData);

        try {
            // Show loading page
            this.showPage('page-personas');

            // Call create-personas API (Vladimir's endpoint)
            const response = await fetch(`${this.apiBaseUrl}/create-personas`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.businessData)
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const result = await response.json();
            console.log('🧠 Personas received:', result);

            if (result.success && result.data && result.data.personas) {
                this.personas = result.data.personas;
                this.populatePersonasEditor();
            } else {
                throw new Error('Invalid personas response');
            }

        } catch (error) {
            console.error('❌ Error generating personas:', error);
            this.showError('A apărut o problemă la generarea personelor. Te rugăm să încerci din nou.');
        }
    }

    // Populate personas editor with received data
    populatePersonasEditor() {
        const container = document.getElementById('personas-container');
        if (!container) return;

        console.log('👥 Populating personas editor...');
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
            <h4>👤 Persona ${index + 1}: ${persona.name}</h4>
            
            <div class="persona-field">
                <label>Nume:</label>
                <input type="text" name="name_${index}" value="${persona.name}" />
            </div>
            
            <div class="persona-field">
                <label>Vârsta:</label>
                <input type="text" name="age_range_${index}" value="${persona.age_range}" />
            </div>
            
            <div class="persona-field">
                <label>Demografia:</label>
                <textarea name="demographics_${index}">${persona.demographics}</textarea>
            </div>
            
            <div class="persona-field">
                <label>Interese:</label>
                <textarea name="interests_${index}">${Array.isArray(persona.interests) ? persona.interests.join(', ') : persona.interests}</textarea>
            </div>
            
            <div class="persona-field">
                <label>Probleme (Pain Points):</label>
                <textarea name="pain_points_${index}">${Array.isArray(persona.pain_points) ? persona.pain_points.join(', ') : persona.pain_points}</textarea>
            </div>
            
            <div class="persona-field">
                <label>Comportament de cumpărare:</label>
                <textarea name="buying_behavior_${index}">${persona.buying_behavior}</textarea>
            </div>
            
            <div class="persona-field">
                <label>Platforme preferate:</label>
                <input type="text" name="preferred_platforms_${index}" value="${Array.isArray(persona.preferred_platforms) ? persona.preferred_platforms.join(', ') : persona.preferred_platforms}" />
            </div>
            
            <div class="persona-field">
                <label>Stil de comunicare:</label>
                <textarea name="communication_style_${index}">${persona.communication_style}</textarea>
            </div>
        `;

        return card;
    }

    // Page 2: Handle personas confirmation
    async handleConfirmPersonas() {
        console.log('✅ Confirming personas...');

        // Collect edited persona data
        const editedPersonas = this.collectEditedPersonas();
        console.log('📝 Edited personas:', editedPersonas);

        try {
            // Show campaign page
            this.showPage('page-campaign');

            // Call schedule-campaign API (Nicolae's endpoint + Vladimir's AI)
            const requestData = {
                businessData: this.businessData,
                confirmedPersonas: editedPersonas
            };

            const response = await fetch(`${this.apiBaseUrl}/schedule-campaign`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const result = await response.json();
            console.log('🚀 Campaign result:', result);

            if (result.success && result.data) {
                this.campaignData = result.data;
                this.populateCampaignDashboard();
            } else {
                throw new Error('Invalid campaign response');
            }

        } catch (error) {
            console.error('❌ Error generating campaign:', error);
            this.showError('A apărut o problemă la generarea campaniei. Te rugăm să încerci din nou.');
        }
    }

    // Collect edited persona data from form
    collectEditedPersonas() {
        const editedPersonas = [];
        const container = document.getElementById('personas-container');
        const personaCards = container.querySelectorAll('.persona-card');

        personaCards.forEach((card, index) => {
            const persona = {
                name: card.querySelector(`input[name="name_${index}"]`).value,
                age_range: card.querySelector(`input[name="age_range_${index}"]`).value,
                demographics: card.querySelector(`textarea[name="demographics_${index}"]`).value,
                interests: card.querySelector(`textarea[name="interests_${index}"]`).value.split(',').map(s => s.trim()),
                pain_points: card.querySelector(`textarea[name="pain_points_${index}"]`).value.split(',').map(s => s.trim()),
                buying_behavior: card.querySelector(`textarea[name="buying_behavior_${index}"]`).value,
                preferred_platforms: card.querySelector(`input[name="preferred_platforms_${index}"]`).value.split(',').map(s => s.trim()),
                communication_style: card.querySelector(`textarea[name="communication_style_${index}"]`).value
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
    }

    // Create post card for display
    createPostCard(post, index) {
        const card = document.createElement('div');
        card.className = 'post-card';

        const platformClass = `platform-${post.platform}`;
        const platformText = post.platform === 'both' ? 'Facebook & Instagram' :
            post.platform === 'facebook' ? 'Facebook' : 'Instagram';

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
    }

    // Error handling
    showError(message) {
        console.error('❌ Showing error:', message);
        alert(`❌ Eroare: ${message}`);

        // In a real app, you'd show a proper error modal
        // For now, we'll just reload to start over
        setTimeout(() => {
            if (confirm('Vrei să începi din nou?')) {
                location.reload();
            }
        }, 2000);
    }

    // Utility: Log current state
    logState() {
        console.log('📊 Current app state:', {
            currentPage: this.currentPage,
            businessData: this.businessData,
            personas: this.personas,
            campaignData: this.campaignData
        });
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
        e.returnValue = 'Ești sigur că vrei să părăsești pagina? Progresul va fi pierdut.';
    }
});