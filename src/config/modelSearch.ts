import modelData from '../data/model_prices_and_context_window.json';

export interface ModelCapabilities {
    supports_function_calling?: boolean;
    supports_parallel_function_calling?: boolean;
    supports_vision?: boolean;
    supports_audio_input?: boolean;
    supports_audio_output?: boolean;
    supports_prompt_caching?: boolean;
    supports_response_schema?: boolean;
    supports_system_messages?: boolean;
}

export interface ModelPricing {
    input_cost_per_token?: number;
    output_cost_per_token?: number;
    input_cost_per_character?: number;
    output_cost_per_character?: number;
    input_cost_per_second?: number;
    output_cost_per_second?: number;
    input_cost_per_image?: number;
    output_cost_per_image?: number;
    input_cost_per_audio_token?: number;
    output_cost_per_audio_token?: number;
    input_cost_per_video_per_second?: number;
}

export interface ModelSpec extends ModelCapabilities, ModelPricing {
    max_tokens?: number | string;
    max_input_tokens?: number | string;
    max_output_tokens?: number | string;
    output_vector_size?: number;
    litellm_provider?: string;
    mode?: string;
    source?: string;
    metadata?: Record<string, any>;
}

// Helper function to convert string to number if needed
function toNumber(value: string | number | undefined): number | undefined {
    if (typeof value === 'string') {
        return parseFloat(value);
    }
    return value;
}

export interface SearchCriteria {
    provider?: string;
    mode?: string;
    minContextSize?: number;
    maxContextSize?: number;
    maxInputCostPerToken?: number;
    capabilities?: Partial<ModelCapabilities>;
}

export class ModelSearch {
    private modelData: Record<string, ModelSpec>;

    constructor() {
        // Convert the raw data and handle string values for numeric fields
        this.modelData = Object.entries(modelData as Record<string, any>).reduce((acc, [key, spec]) => {
            if (key !== 'sample_spec') { // Skip the sample spec
                const convertedSpec: ModelSpec = {
                    ...spec,
                    // Only convert if the field exists
                    ...(('max_tokens' in spec) && {
                        max_tokens: toNumber(spec.max_tokens)
                    }),
                    ...(('max_input_tokens' in spec) && {
                        max_input_tokens: toNumber(spec.max_input_tokens)
                    }),
                    ...(('max_output_tokens' in spec) && {
                        max_output_tokens: toNumber(spec.max_output_tokens)
                    })
                };
                acc[key] = convertedSpec;
            }
            return acc;
        }, {} as Record<string, ModelSpec>);
    }

    search(criteria: SearchCriteria): Record<string, ModelSpec> {
        return Object.entries(this.modelData).reduce((matches, [modelName, modelSpec]) => {
            if (this.matchesCriteria(modelSpec, criteria)) {
                matches[modelName] = modelSpec;
            }
            return matches;
        }, {} as Record<string, ModelSpec>);
    }

    private matchesCriteria(model: ModelSpec, criteria: SearchCriteria): boolean {
        // Provider match
        if (criteria.provider && model.litellm_provider !== criteria.provider) {
            return false;
        }

        // Mode match
        if (criteria.mode && model.mode !== criteria.mode) {
            return false;
        }

        // Context size match
        const maxTokens = toNumber(model.max_tokens);
        if (criteria.minContextSize && (!maxTokens || maxTokens < criteria.minContextSize)) {
            return false;
        }
        if (criteria.maxContextSize && (!maxTokens || maxTokens > criteria.maxContextSize)) {
            return false;
        }

        // Cost match
        if (criteria.maxInputCostPerToken && 
            model.input_cost_per_token && 
            model.input_cost_per_token > criteria.maxInputCostPerToken) {
            return false;
        }

        // Capabilities match
        if (criteria.capabilities) {
            for (const [capability, required] of Object.entries(criteria.capabilities)) {
                if (required && !model[capability as keyof ModelCapabilities]) {
                    return false;
                }
            }
        }

        return true;
    }

    // Helper method to get models by provider
    getModelsByProvider(provider: string): Record<string, ModelSpec> {
        return this.search({ provider });
    }

    // Helper method to get models by mode (chat, completion, embedding)
    getModelsByMode(mode: string): Record<string, ModelSpec> {
        return this.search({ mode });
    }

    // Helper method to get models with specific capabilities
    getModelsByCapabilities(capabilities: Partial<ModelCapabilities>): Record<string, ModelSpec> {
        return this.search({ capabilities });
    }

    // Helper method to get models within a context size range
    getModelsByContextSize(minSize: number, maxSize: number): Record<string, ModelSpec> {
        return this.search({ minContextSize: minSize, maxContextSize: maxSize });
    }

    // Helper method to get models by maximum cost
    getModelsByMaxCost(maxInputCostPerToken: number): Record<string, ModelSpec> {
        return this.search({ maxInputCostPerToken });
    }
}

// Export a singleton instance
export const modelSearch = new ModelSearch();

// Example usage:
/*
const chatModels = modelSearch.getModelsByMode('chat');
const openaiModels = modelSearch.getModelsByProvider('openai');
const functionCallingModels = modelSearch.getModelsByCapabilities({ supports_function_calling: true });
const largeContextModels = modelSearch.getModelsByContextSize(32000, Infinity);
const affordableModels = modelSearch.getModelsByMaxCost(0.00001);

// Complex search
const results = modelSearch.search({
    provider: 'openai',
    mode: 'chat',
    minContextSize: 16000,
    capabilities: {
        supports_function_calling: true,
        supports_vision: true
    }
});
*/
