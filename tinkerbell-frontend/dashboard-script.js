// Dashboard Script - Complete functionality for Tinkerbell
const apiBaseUrl = 'http://localhost:8000/auth_app';

// Global state
let currentPage = 'dashboard';
let userData = {
    sites: [],
    personas: [],
    strategies: [],
    posts: [],
    facebookPosts: []
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeForms();
    loadDashboardData();
    setupEventListeners();
});

// Navigation Setup
function initializeNavigation() {
    const navItems = document.querySelectorAll('.nav-item, .action-card');
    
    navItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            if (page) {
                navigateToPage(page);
            }
        });
    });
}

function navigateToPage(page) {
    // Update active nav item
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    document.querySelector(`[data-page="${page}"]`).classList.add('active');
    
    // Hide all pages
    document.querySelectorAll('.content-page').forEach(page => {
        page.classList.remove('active');
    });
    
    // Show target page
    document.getElementById(`${page}-page`).classList.add('active');
    
    // Update page title
    const titles = {
        'dashboard': 'Dashboard',
        'scraping': 'Website Analysis',
        'sites': 'Analyzed Websites',
        'personas': 'Customer Personas',
        'strategies': 'Marketing Strategies',
        'posts': 'Social Media Posts',
        'facebook': 'Facebook Integration',
        'campaigns': 'Campaign Manager'
    };
    
    document.getElementById('page-title').textContent = titles[page] || 'Dashboard';
    currentPage = page;
    
    // Load page-specific data
    loadPageData(page);
}

// Form Initialization
function initializeForms() {
    // Website scraping form
    const scrapingForm = document.getElementById('scraping-form');
    if (scrapingForm) {
        scrapingForm.addEventListener('submit', handleWebsiteScraping);
    }
    
    // Facebook post form
    const facebookForm = document.getElementById('facebook-post-form');
    if (facebookForm) {
        facebookForm.addEventListener('submit', handleFacebookPost);
    }
}

// Event Listeners Setup
function setupEventListeners() {
    // Quick action buttons
    document.querySelectorAll('.action-card').forEach(button => {
        button.addEventListener('click', function() {
            const page = this.getAttribute('data-page');
            if (page) {
                navigateToPage(page);
            }
        });
    });
}

// Data Loading Functions
async function loadDashboardData() {
    showLoading(true);
    
    try {
        // Load all data in parallel
        await Promise.all([
            loadSites(),
            loadPersonas(),
            loadStrategies(),
            loadPosts()
        ]);
        
        updateDashboardStats();
        updateRecentActivity();
        
    } catch (error) {
        console.error('Error loading dashboard data:', error);
        showError('Failed to load dashboard data');
    } finally {
        showLoading(false);
    }
}

async function loadSites() {
    try {
        const response = await fetch(`${apiBaseUrl}/api/sites/`);
        if (response.ok) {
            userData.sites = await response.json();
        }
    } catch (error) {
        console.error('Error loading sites:', error);
    }
}

async function loadPersonas() {
    try {
        const response = await fetch(`${apiBaseUrl}/api/personas/`);
        if (response.ok) {
            userData.personas = await response.json();
        }
    } catch (error) {
        console.error('Error loading personas:', error);
    }
}

async function loadStrategies() {
    try {
        const response = await fetch(`${apiBaseUrl}/api/strategies/`);
        if (response.ok) {
            userData.strategies = await response.json();
        }
    } catch (error) {
        console.error('Error loading strategies:', error);
    }
}

async function loadPosts() {
    try {
        const response = await fetch(`${apiBaseUrl}/api/posts/`);
        if (response.ok) {
            userData.posts = await response.json();
        }
    } catch (error) {
        console.error('Error loading posts:', error);
    }
}

function loadPageData(page) {
    switch (page) {
        case 'sites':
            renderSitesList();
            break;
        case 'personas':
            renderPersonasList();
            break;
        case 'strategies':
            renderStrategiesList();
            break;
        case 'posts':
            renderPostsList();
            break;
        case 'facebook':
            renderFacebookPosts();
            break;
    }
}

// Dashboard Stats Update
function updateDashboardStats() {
    document.getElementById('stat-sites').textContent = userData.sites.length;
    document.getElementById('stat-personas').textContent = userData.personas.length;
    document.getElementById('stat-strategies').textContent = userData.strategies.length;
    document.getElementById('stat-posts').textContent = userData.posts.length;
}

function updateRecentActivity() {
    const activityList = document.getElementById('activity-list');
    let activities = [];
    
    // Add recent activities based on data
    if (userData.sites.length > 0) {
        activities.push({
            icon: 'bi-globe',
            text: `Analyzed ${userData.sites.length} website(s)`,
            time: 'Recently'
        });
    }
    
    if (userData.personas.length > 0) {
        activities.push({
            icon: 'bi-people',
            text: `Generated ${userData.personas.length} customer persona(s)`,
            time: 'Recently'
        });
    }
    
    if (userData.strategies.length > 0) {
        activities.push({
            icon: 'bi-lightbulb',
            text: `Created ${userData.strategies.length} marketing strategy(ies)`,
            time: 'Recently'
        });
    }
    
    if (userData.posts.length > 0) {
        activities.push({
            icon: 'bi-chat-square-text',
            text: `Generated ${userData.posts.length} social media post(s)`,
            time: 'Recently'
        });
    }
    
    if (activities.length === 0) {
        activities.push({
            icon: 'bi-info-circle',
            text: 'Welcome to Tinkerbell! Start by analyzing a website.',
            time: 'Just now'
        });
    }
    
    activityList.innerHTML = activities.map(activity => `
        <div class="activity-item">
            <i class="${activity.icon}"></i>
            <span>${activity.text}</span>
            <time>${activity.time}</time>
        </div>
    `).join('');
}

// Website Scraping Handler
async function handleWebsiteScraping(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const websiteUrl = formData.get('websiteUrl');
    
    showLoading(true);
    
    try {
        const response = await fetch(`${apiBaseUrl}/scrape-website/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ url: websiteUrl })
        });
        
        if (response.ok) {
            const result = await response.json();
            displayScrapingResults(result);
            
            // Add to sites list
            userData.sites.push({
                url: websiteUrl,
                title: result.title || websiteUrl,
                analyzed_at: new Date().toISOString(),
                content: result
            });
            
            updateDashboardStats();
            showSuccess('Website analyzed successfully!');
        } else {
            throw new Error('Failed to analyze website');
        }
        
    } catch (error) {
        console.error('Error scraping website:', error);
        showError('Failed to analyze website. Please try again.');
    } finally {
        showLoading(false);
    }
}

function displayScrapingResults(result) {
    const resultsDiv = document.getElementById('scraping-results');
    const contentDiv = document.getElementById('analysis-content');
    
    contentDiv.innerHTML = `
        <div class="analysis-summary">
            <h4>${result.title || 'Website Analysis'}</h4>
            <div class="analysis-grid">
                <div class="analysis-item">
                    <strong>Meta Description:</strong>
                    <p>${result.meta_description || 'Not available'}</p>
                </div>
                <div class="analysis-item">
                    <strong>Keywords:</strong>
                    <p>${result.keywords ? result.keywords.join(', ') : 'Not available'}</p>
                </div>
                <div class="analysis-item">
                    <strong>Content Summary:</strong>
                    <p>${result.content_summary || 'Analysis in progress...'}</p>
                </div>
            </div>
        </div>
    `;
    
    resultsDiv.style.display = 'block';
}

// Personas Generation
async function generatePersonas() {
    if (userData.sites.length === 0) {
        showError('Please analyze at least one website first.');
        navigateToPage('scraping');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${apiBaseUrl}/generate-personas-view/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                site_data: userData.sites[0] // Use first site for now
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            
            // Add personas to userData
            if (result.personas) {
                userData.personas = result.personas;
                renderPersonasList();
                updateDashboardStats();
                showSuccess('Customer personas generated successfully!');
            }
        } else {
            throw new Error('Failed to generate personas');
        }
        
    } catch (error) {
        console.error('Error generating personas:', error);
        showError('Failed to generate personas. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Strategy Generation
async function generateStrategy() {
    if (userData.personas.length === 0) {
        showError('Please generate customer personas first.');
        navigateToPage('personas');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${apiBaseUrl}/generate-strategy/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                personas: userData.personas
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            
            userData.strategies.push({
                id: Date.now(),
                title: result.title || 'Marketing Strategy',
                content: result.strategy,
                created_at: new Date().toISOString()
            });
            
            renderStrategiesList();
            updateDashboardStats();
            showSuccess('Marketing strategy generated successfully!');
        } else {
            throw new Error('Failed to generate strategy');
        }
        
    } catch (error) {
        console.error('Error generating strategy:', error);
        showError('Failed to generate strategy. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Posts Generation
async function generatePosts() {
    if (userData.strategies.length === 0) {
        showError('Please create a marketing strategy first.');
        navigateToPage('strategies');
        return;
    }
    
    showLoading(true);
    
    try {
        const response = await fetch(`${apiBaseUrl}/generate-posts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                strategy: userData.strategies[0]
            })
        });
        
        if (response.ok) {
            const result = await response.json();
            
            if (result.posts) {
                userData.posts = userData.posts.concat(result.posts);
                renderPostsList();
                updateDashboardStats();
                showSuccess('Social media posts generated successfully!');
            }
        } else {
            throw new Error('Failed to generate posts');
        }
        
    } catch (error) {
        console.error('Error generating posts:', error);
        showError('Failed to generate posts. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Facebook Post Handler
async function handleFacebookPost(e) {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const content = formData.get('content');
    const image = formData.get('image');
    
    showLoading(true);
    
    try {
        const postData = new FormData();
        postData.append('content', content);
        if (image && image.size > 0) {
            postData.append('image', image);
        }
        
        const response = await fetch(`${apiBaseUrl}/facebook-post/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCsrfToken()
            },
            body: postData
        });
        
        if (response.ok) {
            const result = await response.json();
            
            userData.facebookPosts.push({
                id: Date.now(),
                content: content,
                posted_at: new Date().toISOString(),
                status: 'published'
            });
            
            renderFacebookPosts();
            showSuccess('Post published to Facebook successfully!');
            e.target.reset();
        } else {
            throw new Error('Failed to post to Facebook');
        }
        
    } catch (error) {
        console.error('Error posting to Facebook:', error);
        showError('Failed to post to Facebook. Please try again.');
    } finally {
        showLoading(false);
    }
}

// Render Functions
function renderSitesList() {
    const container = document.getElementById('sites-list');
    
    if (userData.sites.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-globe"></i>
                <h3>No websites analyzed yet</h3>
                <p>Start by analyzing your first website</p>
                <button class="btn btn-primary" onclick="navigateToPage('scraping')">Analyze Website</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = userData.sites.map(site => `
        <div class="list-item">
            <h4>${site.title}</h4>
            <p>${site.url}</p>
            <p>Analyzed: ${new Date(site.analyzed_at).toLocaleDateString()}</p>
            <div class="list-item-actions">
                <button class="btn btn-secondary btn-sm" onclick="viewSiteDetails('${site.url}')">
                    <i class="bi bi-eye"></i> View Details
                </button>
                <button class="btn btn-danger btn-sm" onclick="deleteSite('${site.url}')">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </div>
        </div>
    `).join('');
}

function renderPersonasList() {
    const container = document.getElementById('personas-list');
    
    if (userData.personas.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-people"></i>
                <h3>No personas created yet</h3>
                <p>Generate AI-powered customer personas to understand your audience</p>
                <button class="btn btn-primary" onclick="generatePersonas()">Generate Personas</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = userData.personas.map((persona, index) => `
        <div class="list-item">
            <h4>${persona.name || `Persona ${index + 1}`}</h4>
            <p><strong>Age:</strong> ${persona.age || 'N/A'}</p>
            <p><strong>Interests:</strong> ${persona.interests || 'N/A'}</p>
            <p><strong>Pain Points:</strong> ${persona.pain_points || 'N/A'}</p>
            <div class="list-item-actions">
                <button class="btn btn-secondary btn-sm" onclick="viewPersonaDetails(${index})">
                    <i class="bi bi-eye"></i> View Details
                </button>
                <button class="btn btn-primary btn-sm" onclick="exportPersona(${index})">
                    <i class="bi bi-download"></i> Export
                </button>
            </div>
        </div>
    `).join('');
}

function renderStrategiesList() {
    const container = document.getElementById('strategies-list');
    
    if (userData.strategies.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-lightbulb"></i>
                <h3>No strategies created yet</h3>
                <p>Create AI-powered marketing strategies based on your personas</p>
                <button class="btn btn-primary" onclick="generateStrategy()">Generate Strategy</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = userData.strategies.map((strategy, index) => `
        <div class="list-item">
            <h4>${strategy.title}</h4>
            <p>${strategy.content ? strategy.content.substring(0, 200) + '...' : 'Strategy content'}</p>
            <p>Created: ${new Date(strategy.created_at).toLocaleDateString()}</p>
            <div class="list-item-actions">
                <button class="btn btn-secondary btn-sm" onclick="viewStrategyDetails(${index})">
                    <i class="bi bi-eye"></i> View Details
                </button>
                <button class="btn btn-primary btn-sm" onclick="generatePostsFromStrategy(${index})">
                    <i class="bi bi-chat-square-text"></i> Generate Posts
                </button>
            </div>
        </div>
    `).join('');
}

function renderPostsList() {
    const container = document.getElementById('posts-list');
    
    if (userData.posts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-chat-square-text"></i>
                <h3>No posts generated yet</h3>
                <p>Generate AI-powered social media posts from your strategies</p>
                <button class="btn btn-primary" onclick="generatePosts()">Generate Posts</button>
            </div>
        `;
        return;
    }
    
    container.innerHTML = userData.posts.map((post, index) => `
        <div class="list-item">
            <h4>Social Media Post ${index + 1}</h4>
            <p>${post.content ? post.content.substring(0, 200) + '...' : 'Post content'}</p>
            <div class="list-item-actions">
                <button class="btn btn-secondary btn-sm" onclick="viewPostDetails(${index})">
                    <i class="bi bi-eye"></i> View Details
                </button>
                <button class="btn btn-primary btn-sm" onclick="publishToFacebook(${index})">
                    <i class="bi bi-facebook"></i> Publish
                </button>
            </div>
        </div>
    `).join('');
}

function renderFacebookPosts() {
    const container = document.getElementById('facebook-posts-list');
    
    if (userData.facebookPosts.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-facebook"></i>
                <h3>No posts published yet</h3>
                <p>Your Facebook posts will appear here</p>
            </div>
        `;
        return;
    }
    
    container.innerHTML = userData.facebookPosts.map((post, index) => `
        <div class="list-item">
            <h4>Facebook Post</h4>
            <p>${post.content.substring(0, 200)}${post.content.length > 200 ? '...' : ''}</p>
            <p>Published: ${new Date(post.posted_at).toLocaleDateString()}</p>
            <div class="list-item-actions">
                <span class="badge badge-success">Published</span>
            </div>
        </div>
    `).join('');
}

// Utility Functions
function showLoading(show) {
    const overlay = document.getElementById('loading-overlay');
    overlay.style.display = show ? 'flex' : 'none';
}

function showSuccess(message) {
    // Implementation for success notification
    console.log('Success:', message);
    alert(message); // Temporary - replace with proper notification
}

function showError(message) {
    // Implementation for error notification
    console.error('Error:', message);
    alert(message); // Temporary - replace with proper notification
}

function getCsrfToken() {
    // Get CSRF token from Django
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue || 'dummy-csrf-token';
}

// Action Functions
function viewSiteDetails(url) {
    const site = userData.sites.find(s => s.url === url);
    if (site) {
        // Implementation for viewing site details
        console.log('View site details:', site);
    }
}

function deleteSite(url) {
    if (confirm('Are you sure you want to delete this site analysis?')) {
        userData.sites = userData.sites.filter(s => s.url !== url);
        renderSitesList();
        updateDashboardStats();
    }
}

function viewPersonaDetails(index) {
    const persona = userData.personas[index];
    if (persona) {
        // Implementation for viewing persona details
        console.log('View persona details:', persona);
    }
}

function exportPersona(index) {
    const persona = userData.personas[index];
    if (persona) {
        const dataStr = JSON.stringify(persona, null, 2);
        const dataBlob = new Blob([dataStr], {type: 'application/json'});
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `persona-${index + 1}.json`;
        link.click();
    }
}

function viewStrategyDetails(index) {
    const strategy = userData.strategies[index];
    if (strategy) {
        // Implementation for viewing strategy details
        console.log('View strategy details:', strategy);
    }
}

function generatePostsFromStrategy(index) {
    // Implementation for generating posts from specific strategy
    generatePosts();
}

function viewPostDetails(index) {
    const post = userData.posts[index];
    if (post) {
        // Implementation for viewing post details
        console.log('View post details:', post);
    }
}

function publishToFacebook(index) {
    const post = userData.posts[index];
    if (post) {
        // Pre-fill Facebook form with post content
        navigateToPage('facebook');
        setTimeout(() => {
            document.getElementById('post-content').value = post.content;
        }, 100);
    }
}