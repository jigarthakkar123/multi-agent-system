import React from 'react';
import {
  LayoutDashboard,
  Bot,
  LineChart,
  Users,
  CheckSquare,
  FileText,
  MessageSquare,
  Settings,
  Database
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, pendingApprovalsCount = 0 }) {
  const navItems = [
    { id: 'overview', label: 'Executive Overview', icon: LayoutDashboard },
    { id: 'agents', label: 'Multi-Agent Center', icon: Bot, badge: '6 Agents' },
    { id: 'analytics', label: 'Market & Finance', icon: LineChart },
    { id: 'brokers', label: 'Leads & Brokers', icon: Users },
    {
      id: 'approvals',
      label: 'Human Approvals',
      icon: CheckSquare,
      badge: pendingApprovalsCount > 0 ? `${pendingApprovalsCount} Pending` : null,
      badgeColor: 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
    },
    { id: 'reports', label: 'BI Reports & PDF', icon: FileText },
    { id: 'chat', label: 'AI Business Chat', icon: MessageSquare },
    { id: 'profile', label: 'Profile & Dataset', icon: Database },
  ];

  return (
    <aside className="w-64 min-h-[calc(100vh-61px)] glass-panel border-r border-slate-800/80 bg-slate-950/50 flex flex-col justify-between p-4">
      <div className="space-y-6">
        <div>
          <div className="px-3 mb-2 text-[10px] font-semibold tracking-wider text-slate-400 uppercase">
            Intelligence Modules
          </div>
          <nav className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/25 font-semibold'
                      : 'text-slate-300 hover:text-white hover:bg-slate-800/60'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={`px-1.5 py-0.5 text-[9px] font-bold rounded-md ${
                        item.badgeColor || (isActive ? 'bg-indigo-500 text-white' : 'bg-slate-800 text-indigo-300 border border-indigo-500/20')
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Dataset Scope Card */}
        <div className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-xs">
          <div className="font-semibold text-slate-200 mb-1 flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Dataset Scope
          </div>
          <p className="text-[11px] text-slate-400 leading-relaxed mb-2">
            Synthetic Real Estate data: 1,200 Properties, 1,800 Leads, 600 Deals (May–Oct 2026).
          </p>
          <div className="text-[10px] text-indigo-400 font-mono">Currency: INR (₹)</div>
        </div>
      </div>

      {/* Version Footer */}
      <div className="pt-4 border-t border-slate-800/80 text-[11px] text-slate-500 flex items-center justify-between">
        <span>AGY v2.0 • Real Estate</span>
        <span className="text-emerald-400 font-medium">100/100 Target</span>
      </div>
    </aside>
  );
}
