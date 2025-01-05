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
  return `custom_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
