export const permissions = {
  Admin: ["Dashboard", "Customers", "Products", "Subscription Plans", "Quotations", "Subscriptions", "Invoices", "Payments", "Taxes & Discounts", "Reports", "Staff", "Settings"],
  "Internal Staff": ["Dashboard", "Customers", "Products", "Subscription Plans", "Quotations", "Subscriptions", "Invoices", "Payments", "Reports"],
  Customer: ["Dashboard", "My Profile", "My Subscriptions", "My Invoices", "My Payments", "Notifications", "Account Settings"],
};

export const canAccess = (role, module) => permissions[role]?.includes(module);
