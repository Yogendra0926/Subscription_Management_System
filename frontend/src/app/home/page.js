import "./home.css";
import { ArrowRight, BarChart3, CreditCard, RefreshCw, Users } from "lucide-react";

export default function HomeLanding() {
  return <main className="landing-page">
    <header><a className="landing-brand" href="/home"><b>b</b>brightloop</a><nav><a href="#home">Home</a><a href="#about">About</a><a href="#features">Features</a><a href="#contact">Contact</a></nav><a className="landing-button outline" href="/login">Sign in</a></header>
    <section id="home" className="landing-hero"><p>SUBSCRIPTION MANAGEMENT, REFINED</p><h1>Control recurring revenue<br/><em>with complete clarity.</em></h1><span>Brightloop brings subscriptions, customers, invoices, and payments into one reliable enterprise workspace.</span><div><a className="landing-button" href="/login">Create customer account <ArrowRight size={16}/></a><a className="landing-text-link" href="#features">Explore the platform</a></div><article><section><small>MONTHLY RECURRING REVENUE</small><strong>$38,420</strong><i>↗ 12.4% from last month</i></section><b>▁▂▃▅▄▆▇</b></article></section>
    <section id="about" className="landing-about"><p>BUILT FOR MODERN OPERATIONS</p><h2>One source of truth for<br/>your subscription business.</h2><span>From a new quotation through renewal and payment collection, Brightloop gives finance and operations teams the context to act with confidence.</span></section>
    <section id="features" className="landing-features">{[[RefreshCw,"Subscription lifecycle","Manage plans, renewals, pauses, upgrades, and lifecycle stages from one organized workflow."],[CreditCard,"Billing & payments","Track invoices, payment history, outstanding balances, taxes, and discounts with clarity."],[BarChart3,"Revenue intelligence","Turn customer and billing data into a concise, actionable view of recurring revenue."],[Users,"Customer workspace","Give customers a focused portal for their own invoices and subscriptions."]].map(([Icon,title,text])=><article key={title}><Icon/><h3>{title}</h3><p>{text}</p></article>)}</section>
    <section id="contact" className="landing-final"><h2>Make subscription operations<br/><em>your advantage.</em></h2><a className="landing-button" href="/login">Start with Brightloop <ArrowRight size={16}/></a></section><footer>© 2026 Brightloop Software <span>Privacy · Terms · Security</span></footer>
  </main>;
}
