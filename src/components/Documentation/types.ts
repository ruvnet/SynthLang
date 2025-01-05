import { LucideIcon } from "lucide-react";

export interface DocItem {
  title: string;
  text?: string;
  items?: string[];
  example?: string;
  code?: string;
  component?: () => JSX.Element;
}

export interface DocSection {
  title: string;
  icon: LucideIcon;
  content: DocItem[];
}

// Helper type for component props
export interface DocSectionProps {
  item: DocItem;
}

// Helper type for section props
export interface DocSectionComponentProps {
  section: DocSection;
}
