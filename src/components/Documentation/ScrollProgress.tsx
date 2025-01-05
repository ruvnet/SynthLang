import { useScrollProgress } from "./ScrollToTop";

export const ScrollProgress = () => {
  const progress = useScrollProgress();
  
  return (
    <div className="fixed top-0 left-0 w-full h-1 bg-border/20 z-50">
      <div 
        className="h-full transition-all duration-150"
        style={{ 
          width: `${progress}%`,
          backgroundImage: `linear-gradient(
            to right,
            rgba(168, 85, 247, 0.3),
            rgba(168, 85, 247, 0.5)
          )`,
          boxShadow: `0 0 8px rgba(168, 85, 247, 0.3)`
        }}
      />
      <div 
        className="absolute top-0 right-0 -mr-1 w-2 h-2 rounded-full bg-purple-500/50 
                   shadow-lg shadow-purple-500/20 transition-all duration-150"
        style={{ 
          transform: `translateX(${progress}%)` 
        }}
      />
    </div>
  );
};

export const ScrollProgressProvider = ({ children }: { children: React.ReactNode }) => {
  return (
    <>
      <ScrollProgress />
      {children}
    </>
  );
};
