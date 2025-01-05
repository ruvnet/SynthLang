export const DocSectionSkeleton = () => {
  return (
    <div className="glass-panel p-6 rounded-lg border border-border/40 bg-card/30 backdrop-blur animate-pulse">
      <div className="h-6 w-1/3 bg-purple-500/20 rounded mb-4" />
      <div className="space-y-3">
        <div className="h-4 w-full bg-purple-500/10 rounded" />
        <div className="h-4 w-5/6 bg-purple-500/10 rounded" />
        <div className="h-4 w-4/6 bg-purple-500/10 rounded" />
      </div>
      <div className="mt-6 h-24 w-full bg-black/20 rounded" />
    </div>
  );
};

export const DocSectionSkeletonGroup = () => {
  return (
    <div className="grid gap-6">
      {[...Array(3)].map((_, i) => (
        <DocSectionSkeleton key={i} />
      ))}
    </div>
  );
};
