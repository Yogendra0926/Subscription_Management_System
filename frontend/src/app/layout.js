import "./globals.css";
import "./production.css";

export const metadata = {
  title: "BrightLoop Subscription Management",
  description: "MongoDB-backed subscription management dashboard",
};

export default function RootLayout({ children }) {
  return (
    <html
      lang="en"
      className="h-full antialiased"
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
