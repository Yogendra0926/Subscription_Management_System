import "./globals.css";
import "./production.css";

export const metadata = {
  title: "Brightloop | Subscription Management",
  description: "Brightloop enterprise subscription management workspace",
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
