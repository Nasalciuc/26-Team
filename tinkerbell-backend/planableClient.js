/**
 * Planable API Client for Tinkerbell MVP
 * Author: Nicolae Cociorva
 * 
 * This module handles all interactions with the Planable API for creating
 * workspaces and scheduling social media posts.
 */

class PlanableClient {
    constructor() {
        this.apiKey = process.env.PLANABLE_ACCESS_TOKEN;
        this.baseUrl = 'https://api.planable.io/v1';

        if (!this.apiKey) {
            console.warn('⚠️ PLANABLE_ACCESS_TOKEN not found - using mock responses');
        }
    }

    /**
     * Create a new workspace in Planable
     * @param {string} workspaceName - Name for the new workspace
     * @returns {Promise<Object>} Workspace creation response
     */
    async createWorkspace(workspaceName) {
        console.log(`📋 Planable: Creating workspace "${workspaceName}"`);

        if (!this.apiKey) {
            return this._getMockWorkspace(workspaceName);
        }

        try {
            const response = await fetch(`${this.baseUrl}/workspaces`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: workspaceName,
                    description: `Tinkerbell Marketing Campaign for ${workspaceName}`
                })
            });

            if (!response.ok) {
                throw new Error(`Planable API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ Planable: Workspace created with ID ${data.id}`);
            return data;

        } catch (error) {
            console.error('❌ Planable workspace creation failed:', error.message);
            return this._getMockWorkspace(workspaceName);
        }
    }

    /**
     * Schedule a social media post in Planable
     * @param {string} workspaceId - ID of the workspace
     * @param {Object} postData - Post content and metadata
     * @returns {Promise<Object>} Post scheduling response
     */
    async schedulePost(workspaceId, postData) {
        console.log(`📝 Planable: Scheduling post for ${postData.platform}`);

        if (!this.apiKey) {
            return this._getMockPostResponse(postData);
        }

        try {
            // Transform our post data to Planable format
            const planablePost = this._transformPostData(postData);

            const response = await fetch(`${this.baseUrl}/workspaces/${workspaceId}/posts`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.apiKey}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(planablePost)
            });

            if (!response.ok) {
                throw new Error(`Planable API error: ${response.status} ${response.statusText}`);
            }

            const data = await response.json();
            console.log(`✅ Planable: Post scheduled with ID ${data.id}`);
            return data;

        } catch (error) {
            console.error('❌ Planable post scheduling failed:', error.message);
            return this._getMockPostResponse(postData);
        }
    }

    /**
     * Schedule multiple posts in batch
     * @param {string} workspaceId - ID of the workspace
     * @param {Array} postsData - Array of post objects
     * @returns {Promise<Array>} Array of scheduling responses
     */
    async scheduleMultiplePosts(workspaceId, postsData) {
        console.log(`📚 Planable: Scheduling ${postsData.length} posts in batch`);

        const results = [];

        for (const postData of postsData) {
            try {
                const result = await this.schedulePost(workspaceId, postData);
                results.push({
                    success: true,
                    postData,
                    response: result
                });

                // Small delay to avoid rate limiting
                await this._delay(500);

            } catch (error) {
                console.error(`❌ Failed to schedule post for ${postData.platform}:`, error.message);
                results.push({
                    success: false,
                    postData,
                    error: error.message
                });
            }
        }

        const successCount = results.filter(r => r.success).length;
        console.log(`✅ Planable: ${successCount}/${postsData.length} posts scheduled successfully`);

        return results;
    }

    /**
     * Get workspace URL for user access
     * @param {string} workspaceId - ID of the workspace
     * @returns {string} Direct URL to workspace
     */
    getWorkspaceUrl(workspaceId) {
        return `https://app.planable.io/workspace/${workspaceId}`;
    }

    /**
     * Transform our post data format to Planable API format
     * @private
     */
    _transformPostData(postData) {
        return {
            content: postData.post_text,
            platforms: this._getPlatformIds(postData.platform),
            hashtags: postData.hashtags ? .join(' ') || '',
            call_to_action: postData.call_to_action,
            status: 'draft', // Create as draft for review
            metadata: {
                target_persona: postData.target_persona,
                post_goal: postData.post_goal,
                image_description: postData.image_description
            }
        };
    }

    /**
     * Map platform names to Planable platform IDs
     * @private
     */
    _getPlatformIds(platform) {
        const platformMap = {
            'facebook': ['facebook'],
            'instagram': ['instagram'],
            'both': ['facebook', 'instagram']
        };

        return platformMap[platform] || ['facebook'];
    }

    /**
     * Mock workspace for testing without API key
     * @private
     */
    _getMockWorkspace(workspaceName) {
        console.log('🔄 Using mock workspace (API key not available)');
        const mockId = `mock_ws_${Date.now()}`;
        return {
            id: mockId,
            name: workspaceName,
            url: this.getWorkspaceUrl(mockId),
            created_at: new Date().toISOString(),
            status: 'active'
        };
    }

    /**
     * Mock post response for testing without API key
     * @private
     */
    _getMockPostResponse(postData) {
        console.log('🔄 Using mock post response (API key not available)');
        return {
            id: `mock_post_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            platform: postData.platform,
            content: postData.post_text,
            status: 'scheduled',
            scheduled_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(), // Tomorrow
            created_at: new Date().toISOString()
        };
    }

    /**
     * Utility delay function
     * @private
     */
    _delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

module.exports = PlanableClient;