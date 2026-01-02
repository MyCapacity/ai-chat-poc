import type { Metadata } from "next";

import "./globals.css";
import "@copilotkit/react-ui/styles.css";
import { CopilotKit } from "@copilotkit/react-core";

export const metadata: Metadata = {
  title: "Advanced Analytics Agent",
  description: "Agent UI",
};

function Header() {
  return (
    <div className="py-1 px-5 sticky z-100 border-solid border-1 font-bold border-[#ead3b7ff] border-x-0 border-t-0">
      <h1 className="text-[#9c8060ff] text-sm">Advanced Analytics Agent</h1>
    </div>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={"antialiased"}>
        <Header/>
        {children}
      </body>
    </html>
  );
}
