import { useEffect, useCallback, RefObject } from 'react';

interface KeyCombo {
  key: string;
  ctrl?: boolean;
  meta?: boolean;
  shift?: boolean;
  alt?: boolean;
}

interface ShortcutHandler extends KeyCombo {
  handler: () => void;
  preventDefault?: boolean;
  description?: string;
  group?: string;
}

interface UseKeyboardShortcutsOptions {
  ignoreInputs?: boolean;
  ignoreWhenModalOpen?: boolean;
  modalRef?: RefObject<HTMLElement>;
}

const defaultOptions: UseKeyboardShortcutsOptions = {
  ignoreInputs: true,
  ignoreWhenModalOpen: true
};

export const useKeyboardShortcuts = (
  shortcuts: ShortcutHandler[],
  options: UseKeyboardShortcutsOptions = defaultOptions
) => {
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    // Skip if in input or textarea and ignoreInputs is true
    if (options.ignoreInputs && 
        (document.activeElement?.tagName === 'INPUT' || 
         document.activeElement?.tagName === 'TEXTAREA')) {
      return;
    }

    // Skip if modal is open and ignoreWhenModalOpen is true
    if (options.ignoreWhenModalOpen && 
        options.modalRef?.current?.contains(document.activeElement)) {
      return;
    }

    shortcuts.forEach(shortcut => {
      const keyMatches = e.key.toLowerCase() === shortcut.key.toLowerCase();
      const ctrlMatches = !!shortcut.ctrl === e.ctrlKey;
      const metaMatches = !!shortcut.meta === e.metaKey;
      const shiftMatches = !!shortcut.shift === e.shiftKey;
      const altMatches = !!shortcut.alt === e.altKey;

      if (keyMatches && ctrlMatches && metaMatches && shiftMatches && altMatches) {
        if (shortcut.preventDefault !== false) {
          e.preventDefault();
        }
        shortcut.handler();
      }
    });
  }, [shortcuts, options]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  // Return a function to get all shortcuts for a specific group
  const getShortcutsByGroup = useCallback((group: string) => {
    return shortcuts.filter(s => s.group === group);
  }, [shortcuts]);

  // Return a function to get all shortcuts
  const getAllShortcuts = useCallback(() => {
    return shortcuts.reduce((acc, shortcut) => {
      const group = shortcut.group || 'Other';
      if (!acc[group]) {
        acc[group] = [];
      }
      acc[group].push({
        keys: [
          shortcut.ctrl && 'Ctrl',
          shortcut.meta && 'Cmd',
          shortcut.shift && 'Shift',
          shortcut.alt && 'Alt',
          shortcut.key
        ].filter(Boolean) as string[],
        description: shortcut.description || ''
      });
      return acc;
    }, {} as Record<string, Array<{ keys: string[]; description: string }>>);
  }, [shortcuts]);

  return {
    getShortcutsByGroup,
    getAllShortcuts
  };
};

// Helper function to format key combinations
export const formatKeyCombo = (keys: string[]) => {
  return keys.map(key => {
    switch (key.toLowerCase()) {
      case 'ctrl':
        return '⌃';
      case 'cmd':
        return '⌘';
      case 'shift':
        return '⇧';
      case 'alt':
        return '⌥';
      case 'enter':
        return '↵';
      case 'arrowleft':
        return '←';
      case 'arrowright':
        return '→';
      case 'arrowup':
        return '↑';
      case 'arrowdown':
        return '↓';
      case 'escape':
        return 'Esc';
      default:
        return key.length === 1 ? key.toUpperCase() : key;
    }
  }).join(' + ');
};
