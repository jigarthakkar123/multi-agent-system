import React from 'react';
import { Sparkles, Building2, ShieldCheck, UserCheck, LogOut, LogIn, FileDown, Play } from 'lucide-react';

export default function Navbar({ user, onOpenAuth, onLogout, onTriggerAgents, runningAgents, onDownloadReport }) {
  return (
    <header className="sticky top-0 z-30 flex items-center justify-between px-6 py-3.5 glass-panel border-b border-slate-800/80 bg-slate-950/85 backdrop-blur-md">
      {/* Brand & System Title */}
      <div className="flex items-center gap-3">
        <div className="flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-cyan-400 text-white shadow-lg shadow-indigo-500/20">
          <Building2 className="w-5 h-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-base font-bold tracking-tight text-white">
              Apex Realty Intelligence
            </h1>
            <span className="px-2 py-0.5 text-[10px] font-semibold tracking-wide uppercase bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-full">
              CrewAI 2.0
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Real Estate Operations & Decision Intelligence System
          </p>
        </div>
      </div>

      {/* Action Controls & Auth Status */}
      <div className="flex items-center gap-3">
        {/* Quick Action: Run Multi-Agent System */}
        <button
          onClick={onTriggerAgents}
          disabled={runningAgents}
          className={`flex items-center gap-2 px-3.5 py-1.5 text-xs font-semibold rounded-lg shadow-md transition-all ${
            runningAgents
              ? 'bg-slate-800 text-slate-400 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/25 active:scale-95'
          }`}
        >
          {runningAgents ? (
            <>
              <div className="w-3.5 h-3.5 border-2 border-indigo-300 border-t-transparent rounded-full animate-spin" />
              <span>Agents Running...</span>
            </>
          ) : (
            <>
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Execute 6-Agent Crew</span>
            </>
          )}
        </button>

        {/* Quick Action: Download PDF */}
        <button
          onClick={onDownloadReport}
          className="hidden sm:flex items-center gap-2 px-3 py-1.5 text-xs font-medium text-slate-200 bg-slate-800/80 hover:bg-slate-700/80 border border-slate-700 rounded-lg transition-all active:scale-95"
          title="Download Verified Business Intelligence PDF Report"
        >
          <FileDown className="w-3.5 h-3.5 text-indigo-400" />
          <span>Download PDF</span>
        </button>

        {/* Verification Status Pill */}
        <div className="hidden lg:flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 rounded-lg">
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>Audit: 96.8% Zero-Hallucination</span>
        </div>

        {/* User & Auth Pill */}
        {user ? (
          <div className="flex items-center gap-3 pl-3 border-l border-slate-800">
            <div className="text-right hidden sm:block">
              <div className="text-xs font-medium text-white">{user.full_name || user.email}</div>
              <div className="text-[10px] text-slate-400 capitalize">{user.role || 'Manager'}</div>
            </div>
            <div className="w-8 h-8 rounded-full bg-indigo-500/20 border border-indigo-500/40 text-indigo-300 flex items-center justify-center font-bold text-xs uppercase">
              {(user.full_name || user.email)[0]}
            </div>
            <button
              onClick={onLogout}
              className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
              title="Sign Out"
            >
              <LogOut className="w-4 h-4" />
            </button>
          </div>
        ) : (
          <button
            onClick={onOpenAuth}
            className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-indigo-400 bg-indigo-500/10 hover:bg-indigo-500/20 border border-indigo-500/30 rounded-lg transition-all"
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>
        )}
      </div>
    </header>
  );
}
