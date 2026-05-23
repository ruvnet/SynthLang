import { Framework } from '../components/AdvancedCalculator/types';

const CUSTOM_FRAMEWORKS_KEY = 'synthLang_customFrameworks';

export interface CustomFramework extends Framework {
  id: string;
  createdAt: number;
  updatedAt: number;
}

export const saveCustomFramework = (framework: CustomFramework): void => {
  const existing = getCustomFrameworks();
  const updated = [...existing.filter(f => f.id !== framework.id), framework];
  localStorage.setItem(CUSTOM_FRAMEWORKS_KEY, JSON.stringify(updated));
};

export const getCustomFrameworks = (): CustomFramework[] => {
  try {
    const stored = localStorage.getItem(CUSTOM_FRAMEWORKS_KEY);
    return stored ? JSON.parse(stored) : [];
  } catch (error) {
    console.error('Failed to load custom frameworks:', error);
    return [];
  }
};

export const deleteCustomFramework = (id: string): void => {
  const existing = getCustomFrameworks();
  const updated = existing.filter(f => f.id !== id);
  localStorage.setItem(CUSTOM_FRAMEWORKS_KEY, JSON.stringify(updated));
};

export const generateFrameworkId = (): string => {
  // Use crypto.randomUUID() (available in all modern browsers and Node ≥14.17)
  // to avoid Math.random() which is not cryptographically secure.
  const randomPart =
    typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function'
      ? crypto.randomUUID().replace(/-/g, '').slice(0, 12)
      : Array.from(
          typeof crypto !== 'undefined' && crypto.getRandomValues
            ? crypto.getRandomValues(new Uint8Array(6))
            : new Uint8Array(6)
        )
          .map(b => b.toString(16).padStart(2, '0'))
          .join('');
  return `custom_${Date.now()}_${randomPart}`;
};
