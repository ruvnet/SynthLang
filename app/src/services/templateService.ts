import { useQuery } from "@tanstack/react-query";

export interface Template {
  title: string;
  domain: string;
  category: string;
  overview: string;
  content: string;
}

export const useTemplate = (templateId: string) => {
  return useQuery({
    queryKey: ["template", templateId],
    queryFn: async () => {
      const response = await fetch(`/templates/${templateId}.md`);
      const text = await response.text();
      const [frontmatter, ...contentParts] = text.split('---\n').filter(Boolean);
      
      const metadata = Object.fromEntries(
        frontmatter.split('\n')
          .filter(Boolean)
          .map(line => line.split(': ').map(part => part.trim()))
      );

      return {
        ...metadata,
        content: contentParts.join('---\n')
      } as Template;
    }
  });
};
