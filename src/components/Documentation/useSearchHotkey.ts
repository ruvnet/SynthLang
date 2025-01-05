import { useEffect, useRef } from 'react';

export const useSearchHotkey = (onActivate: () => void) => {
  const isMetaKey = useRef(false);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Meta' || e.key === 'Control') {
        isMetaKey.current = true;
      }
      
      if (isMetaKey.current && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        onActivate();
      }
    };

    const handleKeyUp = (e: KeyboardEvent) => {
      if (e.key === 'Meta' || e.key === 'Control') {
        isMetaKey.current = false;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    window.addEventListener('keyup', handleKeyUp);

    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      window.removeEventListener('keyup', handleKeyUp);
    };
  }, [onActivate]);
};
