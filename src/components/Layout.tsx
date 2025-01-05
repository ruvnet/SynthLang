import React from "react";
import MainNav from "./MainNav";

interface LayoutProps {
  children: React.ReactNode;
  title?: string;
}

const Layout = ({ children, title }: LayoutProps) => {
  return (
    <div className="min-h-screen bg-background">
      <MainNav title={title} />
      <main className="pt-[96px]">{children}</main>
    </div>
  );
};

export default Layout;
