"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { API_URL, apiRequest, login } from "@/lib/api";

const resources = [
  ["products", "Products"],
  ["product-variants", "Product variants"],
  ["subscription-plans", "Subscription plans"],
  ["customers", "Customers"],
  ["subscriptions", "Subscriptions"],
  ["invoices", "Invoices"],
  ["payments", "Payments"],
  ["quotations", "Quotations"],
  ["quotation-lines", "Quotation lines"],
  ["taxes", "Taxes"],
  ["discounts", "Discounts"],
  ["subscription-history", "Subscription history"],
  ["users", "Users"],
];

function formatValue(value) {
  if (value === null || value === undefined) return "—";
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

function Login({ onLogin }) {
  const [email, setEmail] = useState("admin@brightloop.test");
  const [password, setPassword] = useState("Demo@123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setError("");
    setLoading(true);
    try {
      const result = await login(email, password);
      localStorage.setItem("brightloop_token", result.access_token);
      localStorage.setItem("brightloop_user", JSON.stringify(result.user));
      onLogin(result.user);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center bg-slate-950 px-6">
      <form onSubmit={submit} className="w-full max-w-md rounded-3xl bg-white p-8 shadow-2xl">
        <p className="mb-2 text-sm font-semibold uppercase tracking-[0.2em] text-cyan-600">
          BrightLoop
        </p>
        <h1 className="mb-2 text-3xl font-bold text-slate-900">Subscription management</h1>
        <p className="mb-8 text-slate-500">Sign in to manage your MongoDB-backed data.</p>
        <label className="mb-4 block text-sm font-medium text-slate-700">
          Email
          <input value={email} onChange={(event) => setEmail(event.target.value)} type="email"
            className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-cyan-500" required />
        </label>
        <label className="mb-6 block text-sm font-medium text-slate-700">
          Password
          <input value={password} onChange={(event) => setPassword(event.target.value)} type="password"
            className="mt-2 w-full rounded-xl border border-slate-200 px-4 py-3 outline-none focus:border-cyan-500" required />
        </label>
        {error && <p className="mb-4 rounded-lg bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <button disabled={loading} className="w-full rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-cyan-700 disabled:opacity-50">
          {loading ? "Signing in..." : "Sign in"}
        </button>
        <p className="mt-4 text-xs text-slate-400">Demo: admin@brightloop.test / Demo@123!</p>
      </form>
    </main>
  );
}

function Dashboard({ user, onLogout }) {
  const [selected, setSelected] = useState("products");
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState(0);
  const [health, setHealth] = useState("checking");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [payload, setPayload] = useState('{\n  "name": "New record"\n}');

  const label = useMemo(
    () => resources.find(([key]) => key === selected)?.[1] || selected,
    [selected],
  );

  const loadRecords = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const result = await apiRequest(`/api/${selected}?page=1&limit=50`);
      setRecords(result.items || []);
      setTotal(result.total || 0);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setLoading(false);
    }
  }, [selected]);

  useEffect(() => {
    apiRequest("/health").then(() => setHealth("connected")).catch(() => setHealth("offline"));
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      loadRecords();
    }, 0);
    return () => clearTimeout(timer);
  }, [loadRecords]);

  async function createRecord(event) {
    event.preventDefault();
    setError("");
    try {
      await apiRequest(`/api/${selected}`, { method: "POST", body: payload });
      await loadRecords();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  async function deleteRecord(id) {
    if (!window.confirm("Delete this record?")) return;
    try {
      await apiRequest(`/api/${selected}/${id}`, { method: "DELETE" });
      await loadRecords();
    } catch (requestError) {
      setError(requestError.message);
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900">
      <header className="border-b bg-white">
        <div className="mx-auto flex max-w-[1500px] items-center justify-between px-6 py-5">
          <div>
            <p className="text-sm font-bold uppercase tracking-[0.2em] text-cyan-600">BrightLoop</p>
            <h1 className="text-2xl font-bold">Data dashboard</h1>
          </div>
          <div className="flex items-center gap-4">
            <span className="hidden text-sm text-slate-500 sm:block">{user?.email}</span>
            <button onClick={onLogout} className="rounded-lg border px-3 py-2 text-sm font-medium hover:bg-slate-50">Sign out</button>
          </div>
        </div>
      </header>
      <main className="mx-auto grid max-w-[1500px] gap-6 px-6 py-6 lg:grid-cols-[240px_1fr]">
        <aside className="rounded-2xl bg-slate-900 p-3 text-white">
          <div className="mb-3 flex items-center justify-between px-3 py-2 text-sm">
            <span className="text-slate-400">API resources</span>
            <span className={`h-2 w-2 rounded-full ${health === "connected" ? "bg-emerald-400" : "bg-red-400"}`} />
          </div>
          {resources.map(([key, title]) => (
            <button key={key} onClick={() => setSelected(key)}
              className={`mb-1 w-full rounded-lg px-3 py-2 text-left text-sm ${selected === key ? "bg-cyan-600 font-semibold" : "text-slate-300 hover:bg-slate-800"}`}>
              {title}
            </button>
          ))}
        </aside>
        <section className="min-w-0">
          <div className="mb-6 flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="text-sm text-slate-500">Connected to {API_URL}</p>
              <h2 className="text-3xl font-bold">{label}</h2>
            </div>
            <span className="rounded-full bg-white px-4 py-2 text-sm text-slate-600 shadow-sm">{total} records</span>
          </div>
          {error && <div className="mb-4 rounded-xl bg-red-50 p-4 text-sm text-red-700">{error}</div>}
          <div className="grid gap-6 xl:grid-cols-[1fr_360px]">
            <div className="overflow-hidden rounded-2xl bg-white shadow-sm">
              {loading ? <p className="p-6 text-slate-500">Loading records...</p> : records.length === 0 ? (
                <p className="p-6 text-slate-500">No records found.</p>
              ) : (
                <div className="overflow-x-auto">
                  <table className="w-full text-left text-sm">
                    <thead className="bg-slate-50 text-xs uppercase text-slate-500">
                      <tr><th className="px-5 py-4">ID</th><th className="px-5 py-4">Data</th><th className="px-5 py-4">Action</th></tr>
                    </thead>
                    <tbody className="divide-y">
                      {records.map((record) => (
                        <tr key={record._id}>
                          <td className="whitespace-nowrap px-5 py-4 font-mono text-xs text-slate-500">{record._id}</td>
                          <td className="max-w-[520px] px-5 py-4"><pre className="whitespace-pre-wrap text-xs">{JSON.stringify(record, null, 2)}</pre></td>
                          <td className="px-5 py-4"><button onClick={() => deleteRecord(record._id)} className="text-red-600 hover:underline">Delete</button></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
            <form onSubmit={createRecord} className="h-fit rounded-2xl bg-white p-5 shadow-sm">
              <h3 className="mb-1 font-semibold">Create {label.toLowerCase()}</h3>
              <p className="mb-4 text-xs text-slate-500">Send a JSON body to the FastAPI endpoint.</p>
              <textarea value={payload} onChange={(event) => setPayload(event.target.value)}
                className="mb-4 h-64 w-full rounded-xl border border-slate-200 bg-slate-50 p-3 font-mono text-xs outline-none focus:border-cyan-500" />
              <button className="w-full rounded-xl bg-cyan-600 px-4 py-3 font-semibold text-white hover:bg-cyan-700">Create record</button>
            </form>
          </div>
        </section>
      </main>
    </div>
  );
}

export default function Home() {
  const [user, setUser] = useState(null);
  const [ready, setReady] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      const savedUser = localStorage.getItem("brightloop_user");
      const token = localStorage.getItem("brightloop_token");
      if (savedUser && token) setUser(JSON.parse(savedUser));
      setReady(true);
    }, 0);
    return () => clearTimeout(timer);
  }, []);

  function logout() {
    localStorage.removeItem("brightloop_token");
    localStorage.removeItem("brightloop_user");
    setUser(null);
  }

  if (!ready) return <div className="flex min-h-screen items-center justify-center">Loading...</div>;
  return user ? <Dashboard user={user} onLogout={logout} /> : <Login onLogin={setUser} />;
}
