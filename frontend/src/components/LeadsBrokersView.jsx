import React from 'react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';
import { Users, Award, Star, TrendingUp, PhoneCall, CalendarCheck } from 'lucide-react';

export default function LeadsBrokersView({ leadFunnel, leadSources, agentLeaderboard }) {
  return (
    <div className="space-y-6">
      {/* Lead Acquisition & Funnel Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Lead Funnel Pipeline */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Users className="w-4 h-4 text-violet-400" />
              <h3 className="text-sm font-bold text-white">Customer Lead Funnel Progression</h3>
            </div>
            <span className="text-xs text-slate-400">1,800 Total Inquiries</span>
          </div>

          <div className="space-y-3">
            {leadFunnel && leadFunnel.map((stage, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-slate-200">{stage.stage}</span>
                  <div className="flex items-center gap-2">
                    <span className="font-mono text-white">{stage.count} Leads</span>
                    <span className="text-[11px] text-slate-400">({stage.percentage}%)</span>
                  </div>
                </div>
                <div className="w-full h-2 rounded-full bg-slate-800 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-indigo-500 to-cyan-400"
                    style={{ width: `${stage.percentage}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Lead Source Efficiency */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-emerald-400" />
              <h3 className="text-sm font-bold text-white">Lead Generation Channel Conversion Rate</h3>
            </div>
            <span className="text-xs text-slate-400">Highest ROI Channels</span>
          </div>

          <div className="h-60 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={leadSources || []} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" opacity={0.4} />
                <XAxis dataKey="source" stroke="#94A3B8" fontSize={11} />
                <YAxis stroke="#94A3B8" fontSize={11} tickFormatter={(v) => `${v}%`} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '12px', color: '#FFF' }}
                  formatter={(v, name) => [`${v}%`, 'Conversion Rate']}
                />
                <Bar dataKey="conversion_rate" fill="#10B981" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Sales Broker / Agent Leaderboard */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Award className="w-5 h-5 text-amber-400" />
            <div>
              <h3 className="text-sm font-bold text-white">Sales Broker Performance Leaderboard</h3>
              <p className="text-xs text-slate-400">Top agents ranked by brokerage commission generated and customer rating</p>
            </div>
          </div>
          <span className="text-xs font-mono text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-lg border border-indigo-500/20">
            55 Agency Brokers Audited
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800">
              <tr>
                <th className="py-2.5 px-3">Rank / Broker ID</th>
                <th className="py-2.5 px-2 text-center">Calls Logged</th>
                <th className="py-2.5 px-2 text-center">Site Visits</th>
                <th className="py-2.5 px-2 text-center">Deals Closed</th>
                <th className="py-2.5 px-3 text-right">Commission Earned</th>
                <th className="py-2.5 px-2 text-center">Customer Rating</th>
                <th className="py-2.5 px-3 text-right">Marketing Spend</th>
                <th className="py-2.5 px-2 text-right">ROI Multiple</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-mono">
              {agentLeaderboard && agentLeaderboard.map((agent, i) => (
                <tr key={i} className="hover:bg-slate-800/40 transition-colors">
                  <td className="py-2.5 px-3 font-sans font-semibold text-white flex items-center gap-2">
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold ${
                      i === 0 ? 'bg-amber-400 text-slate-950' : i === 1 ? 'bg-slate-300 text-slate-950' : i === 2 ? 'bg-amber-700 text-white' : 'bg-slate-800 text-slate-300'
                    }`}>
                      {i + 1}
                    </span>
                    <span>{agent.agent_id}</span>
                  </td>
                  <td className="py-2.5 px-2 text-center text-slate-300">{agent.total_calls}</td>
                  <td className="py-2.5 px-2 text-center text-slate-300">{agent.total_visits}</td>
                  <td className="py-2.5 px-2 text-center text-emerald-400 font-bold">{agent.deals_closed}</td>
                  <td className="py-2.5 px-3 text-right text-indigo-400 font-semibold">₹{(agent.total_commission_earned / 100000).toFixed(2)} L</td>
                  <td className="py-2.5 px-2 text-center text-amber-300 font-sans flex items-center justify-center gap-1">
                    <Star className="w-3 h-3 fill-current" />
                    <span>{agent.avg_customer_rating}</span>
                  </td>
                  <td className="py-2.5 px-3 text-right text-slate-400">₹{(agent.total_marketing_spend / 1000).toFixed(1)}k</td>
                  <td className="py-2.5 px-2 text-right text-emerald-400 font-bold">{agent.roi_multiple}x</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
