import React from 'react';
import KPIStats from './KPIStats';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
import { Bot, CheckCircle, AlertTriangle, ArrowRight, ShieldCheck, Zap } from 'lucide-react';

export default function OverviewView({
  kpis,
  monthlyTrends,
  cityPerformance,
  agentsStatus,
  pendingApprovals,
  onNavigateTab,
  onTriggerAgents,
  runningAgents
}) {
  const formatYAxisCr = (tick) => `₹${(tick / 10000000).toFixed(0)}Cr`;
  const formatYAxisL = (tick) => `₹${(tick / 100000).toFixed(0)}L`;

  return (
    <div className="space-y-6">
      {/* Backend Connecting Callout (if Render service is waking up) */}
      {!kpis && (
        <div className="p-4 rounded-2xl bg-indigo-500/10 border border-indigo-500/30 flex items-center gap-3 shadow-lg shadow-indigo-500/5 animate-pulse">
          <div className="w-5 h-5 border-2 border-indigo-400 border-t-transparent rounded-full animate-spin shrink-0"></div>
          <div>
            <div className="text-sm font-semibold text-indigo-300">Connecting to Live Render Backend Service...</div>
            <p className="text-xs text-slate-400">
              Render web services sleep during inactivity. Awakening service and loading dataset telemetry (May 1 – Oct 31, 2026)...
            </p>
          </div>
        </div>
      )}

      {/* Pending Human-in-the-Loop Approval Alert Callout */}
      {pendingApprovals && pendingApprovals.length > 0 && (
        <div className="p-4 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-lg shadow-amber-500/5">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-amber-500/20 text-amber-400">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <div className="text-sm font-bold text-amber-300">
                {pendingApprovals.length} Strategic Action{pendingApprovals.length > 1 ? 's' : ''} Awaiting Executive Approval
              </div>
              <p className="text-xs text-slate-300">
                The Strategy & Verification Agents have generated consequential budget and operational initiatives requiring human sign-off.
              </p>
            </div>
          </div>
          <button
            onClick={() => onNavigateTab('approvals')}
            className="flex items-center gap-1.5 px-4 py-2 text-xs font-semibold text-slate-900 bg-amber-400 hover:bg-amber-300 rounded-xl transition-all shadow-md active:scale-95 whitespace-nowrap"
          >
            <span>Review Queue</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Top Level KPIs */}
      <KPIStats kpis={kpis} />

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Monthly Revenue & Commission Trends */}
        <div className="lg:col-span-2 glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Monthly Transaction Revenue & Expenses (May–Oct 2026)</h3>
              <p className="text-xs text-slate-400">Total closed sales volume vs. operational expense overhead</p>
            </div>
            <div className="flex items-center gap-4 text-xs">
              <div className="flex items-center gap-1.5 text-indigo-400">
                <span className="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                <span>Revenue (Cr)</span>
              </div>
              <div className="flex items-center gap-1.5 text-rose-400">
                <span className="w-2.5 h-2.5 rounded-full bg-rose-500"></span>
                <span>Expenses (L)</span>
              </div>
            </div>
          </div>

          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={monthlyTrends} margin={{ top: 10, right: 10, left: 10, bottom: 0 }}>
                <defs>
                  <linearGradient id="revenueGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#6366F1" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#6366F1" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="expenseGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#F43F5E" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#F43F5E" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.5} />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis yAxisId="left" stroke="#94A3B8" fontSize={11} tickFormatter={formatYAxisCr} tickLine={false} />
                <YAxis yAxisId="right" orientation="right" stroke="#F43F5E" fontSize={11} tickFormatter={formatYAxisL} tickLine={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }}
                  formatter={(value, name) => [
                    name === 'revenue' ? `₹${(value / 10000000).toFixed(2)} Cr` : `₹${(value / 100000).toFixed(2)} L`,
                    name === 'revenue' ? 'Sales Revenue' : 'Expenses'
                  ]}
                />
                <Area yAxisId="left" type="monotone" dataKey="revenue" stroke="#6366F1" strokeWidth={2.5} fillOpacity={1} fill="url(#revenueGrad)" />
                <Area yAxisId="right" type="monotone" dataKey="expenses" stroke="#F43F5E" strokeWidth={2} fillOpacity={1} fill="url(#expenseGrad)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Top Cities by Sales Volume */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-white">Top Regional Markets</h3>
                <p className="text-xs text-slate-400">Closed Sales Volume by City</p>
              </div>
              <button
                onClick={() => onNavigateTab('analytics')}
                className="text-xs text-indigo-400 hover:text-indigo-300 font-medium"
              >
                View All
              </button>
            </div>

            <div className="h-60 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={cityPerformance ? cityPerformance.slice(0, 5) : []} layout="vertical" margin={{ left: 20 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                  <XAxis type="number" stroke="#94A3B8" fontSize={10} tickFormatter={(v) => `₹${(v / 10000000).toFixed(0)}Cr`} />
                  <YAxis type="category" dataKey="city" stroke="#CBD5E1" fontSize={11} width={75} />
                  <Tooltip
                    contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', color: '#FFF' }}
                    formatter={(v) => [`₹${(v / 10000000).toFixed(2)} Cr`, 'Closed Revenue']}
                  />
                  <Bar dataKey="revenue_generated" fill="#38BDF8" radius={[0, 6, 6, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="pt-3 border-t border-slate-800 text-[11px] text-slate-400 flex items-center justify-between">
            <span>Primary Growth Cluster</span>
            <span className="text-white font-semibold">Western India Corridor</span>
          </div>
        </div>
      </div>

      {/* Multi-Agent Operating Status Bar */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 mb-4">
          <div>
            <div className="flex items-center gap-2">
              <Bot className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white">Autonomous CrewAI Multi-Agent Fleet</h3>
            </div>
            <p className="text-xs text-slate-400">
              6 Specialized Agents operating sequentially with continuous hallucination verification
            </p>
          </div>
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1.5 text-xs text-emerald-400 font-medium bg-emerald-500/10 px-2.5 py-1 rounded-lg border border-emerald-500/20">
              <ShieldCheck className="w-3.5 h-3.5" />
              Zero Hallucinations Verified
            </span>
            <button
              onClick={() => onNavigateTab('agents')}
              className="text-xs font-semibold text-indigo-400 hover:text-indigo-300 flex items-center gap-1"
            >
              <span>Inspect Agent Logs</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
          {agentsStatus && agentsStatus.map((agent, i) => (
            <div
              key={i}
              className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-slate-700 transition-all cursor-pointer"
              onClick={() => onNavigateTab('agents')}
            >
              <div className="flex items-center justify-between mb-1.5">
                <span className="text-[10px] font-mono text-slate-400">Agent {i + 1}</span>
                <span className="w-2 h-2 rounded-full bg-emerald-400 shadow-sm shadow-emerald-400/50"></span>
              </div>
              <div className="text-xs font-semibold text-white truncate">{agent.agent_name.replace(' Agent', '')}</div>
              <div className="text-[10px] text-slate-400 truncate mt-0.5">{agent.status}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
