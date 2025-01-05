import '@testing-library/jest-dom';

// Mock Vite's import.meta.env
const env = {
  VITE_ENCRYPTION_KEY: 'test-encryption-key',
  VITE_OPENROUTER_KEY: 'test-api-key',
};

global.import = {
  meta: {
    env
  }
} as any;

// Mock window.location
delete window.location;
window.location = {
  origin: 'http://localhost:3000',
  ...window.location
};

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
  length: 0,
  key: jest.fn(),
};
global.localStorage = localStorageMock as Storage;

// Mock crypto
global.crypto = {
  ...global.crypto,
  randomUUID: () => '123e4567-e89b-12d3-a456-426614174000'
};

// Mock TextEncoder/TextDecoder
global.TextEncoder = require('util').TextEncoder;
global.TextDecoder = require('util').TextDecoder;

// Mock ReadableStream if not available
if (typeof ReadableStream === 'undefined') {
  global.ReadableStream = require('stream/web').ReadableStream;
}
