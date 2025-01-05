import { ModelSearch, SearchCriteria } from '../modelSearch';

describe('ModelSearch', () => {
    let modelSearch: ModelSearch;

    beforeEach(() => {
        modelSearch = new ModelSearch();
    });

    test('should find models by provider', () => {
        const openaiModels = modelSearch.getModelsByProvider('openai');
        expect(Object.keys(openaiModels).length).toBeGreaterThan(0);
        Object.values(openaiModels).forEach(model => {
            expect(model.litellm_provider).toBe('openai');
        });
    });

    test('should find models by mode', () => {
        const chatModels = modelSearch.getModelsByMode('chat');
        expect(Object.keys(chatModels).length).toBeGreaterThan(0);
        Object.values(chatModels).forEach(model => {
            expect(model.mode).toBe('chat');
        });
    });

    test('should find models by capabilities', () => {
        const functionCallingModels = modelSearch.getModelsByCapabilities({ 
            supports_function_calling: true 
        });
        expect(Object.keys(functionCallingModels).length).toBeGreaterThan(0);
        Object.values(functionCallingModels).forEach(model => {
            expect(model.supports_function_calling).toBe(true);
        });
    });

    test('should find models by context size range', () => {
        const largeContextModels = modelSearch.getModelsByContextSize(32000, Infinity);
        expect(Object.keys(largeContextModels).length).toBeGreaterThan(0);
        Object.values(largeContextModels).forEach(model => {
            const maxTokens = typeof model.max_tokens === 'string' 
                ? parseInt(model.max_tokens) 
                : model.max_tokens;
            expect(maxTokens).toBeGreaterThanOrEqual(32000);
        });
    });

    test('should find models by maximum cost', () => {
        const affordableModels = modelSearch.getModelsByMaxCost(0.00001);
        expect(Object.keys(affordableModels).length).toBeGreaterThan(0);
        Object.values(affordableModels).forEach(model => {
            if (model.input_cost_per_token) {
                expect(model.input_cost_per_token).toBeLessThanOrEqual(0.00001);
            }
        });
    });

    test('should handle complex search criteria', () => {
        const criteria: SearchCriteria = {
            provider: 'openai',
            mode: 'chat',
            minContextSize: 16000,
            capabilities: {
                supports_function_calling: true,
                supports_vision: true
            }
        };

        const results = modelSearch.search(criteria);
        expect(Object.keys(results).length).toBeGreaterThan(0);
        Object.values(results).forEach(model => {
            expect(model.litellm_provider).toBe('openai');
            expect(model.mode).toBe('chat');
            const maxTokens = typeof model.max_tokens === 'string' 
                ? parseInt(model.max_tokens) 
                : model.max_tokens;
            expect(maxTokens).toBeGreaterThanOrEqual(16000);
            expect(model.supports_function_calling).toBe(true);
            expect(model.supports_vision).toBe(true);
        });
    });

    test('should handle empty search criteria', () => {
        const results = modelSearch.search({});
        // Should return all models except sample_spec
        expect(Object.keys(results).length).toBeGreaterThan(0);
        expect(Object.keys(results)).not.toContain('sample_spec');
    });

    test('should return empty object for non-matching criteria', () => {
        const results = modelSearch.search({
            provider: 'non-existent-provider'
        });
        expect(Object.keys(results).length).toBe(0);
    });

    test('should handle models without token fields', () => {
        const results = modelSearch.search({
            mode: 'image_generation' // These models typically don't have token fields
        });
        expect(Object.keys(results).length).toBeGreaterThan(0);
        Object.values(results).forEach(model => {
            expect(model.mode).toBe('image_generation');
        });
    });
});
