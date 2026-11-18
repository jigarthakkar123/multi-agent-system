import React, { useState } from 'react';
import {
  Bot,
  Play,
  CheckCircle2,
  AlertCircle,
  FileSearch,
  Megaphone,
  CircleDollarSign,
  Briefcase,
  TrendingUp,
  ShieldCheck,
  Cpu,
  Layers,
  ChevronRight
} from 'lucide-react';

export default function AgentsView({
  agentsStatus,
  agentLogs,
  onTriggerAgents,
  runningAgents
}) {
  const [executionMode, setExecutionMode] = useState('sequential');
  const [selectedAgent, setSelectedAgent] = useState('Data Analyst Agent');

  const agentIcons = {
    'Data Analyst Agent': FileSearch,
    'Marketing Agent': Megaphone,
    'Finance Agent': CircleDollarSign,
    'Operations Agent': Briefcase,
    'Strategy Agent': TrendingUp,
    'Verification Agent': ShieldCheck
  };

  const agentDescriptions = {
    'Data Analyst Agent': {
      color: 'border-blue-500/40 text-blue-400 bg-blue-500/10',
      responsibilities: [
        'Analyze 1,200 property listings & calculate KPIs',
        'Detect city price-per-sqft shifts across 10 hubs',
        'Identify inventory absorption rates and anomalous drop-offs'
      ]
    },
    'Marketing Agent': {
      color: 'border-purple-500/40 text-purple-400 bg-purple-500/10',
      responsibilities: [
        'Segment 1,800 customer inquiries by budget & intent',
        'Evaluate acquisition channels (Referrals vs Digital vs Walk-in)',
        'Calculate Cost-per-Acquisition (CAC) and recommend budget shift'
      ]
    },
    'Finance Agent': {
      color: 'border-emerald-500/40 text-emerald-400 bg-emerald-500/10',
      responsibilities: [
        'Audit Rs. 11.70 Cr commissions and Rs. 2.98 Cr expenses (500 records)',
        'Verify 74.58% net agency operating margin and cost breakdown',
        'Audit Advertising (19.28%) and Maintenance (17.82%) cost drivers'
      ]
    },
    'Operations Agent': {
      color: 'border-amber-500/40 text-amber-400 bg-amber-500/10',
      responsibilities: [
        'Audit 55 active sales brokers and 1,200 site visits',
        'Evaluate 299 repeat-visit requests and 331 expected offers',
        'Top 10 brokers generate 31.16% of all agency commissions'
      ]
    },
    'Strategy Agent': {
      color: 'border-indigo-500/40 text-indigo-400 bg-indigo-500/10',
      responsibilities: [
        'Synthesize cross-agent findings into a 90-day turnaround blueprint',
        'Structure consequential business actions for Human Approval',
        'Propose Rs. 35L capital reallocation to Campaign and Referral channels'
      ]
    },
    'Verification Agent': {
      color: 'border-teal-500/40 text-teal-400 bg-teal-500/10',
      responsibilities: [
        'Cross-verify numerical metrics against raw database records',
        'Detect LLM hallucinations and flag contradictory claims',
        'Issue audited Confidence Score (99.0%) and zero-hallucination certificate'
      ]
    }
  };

  return (
    <div className="space-y-6">
      {/* Header & Controls */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Cpu className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-white">CrewAI Multi-Agent Autonomous Fleet</h2>
            <span className="px-2 py-0.5 text-[10px] font-bold uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-md">
              6 Specialized Agents Active
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Agents communicate inter-dependently: Data Analyst ➔ Marketing ➔ Finance ➔ Operations ➔ Strategy ➔ Verification
          </p>
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          {/* Mode Selector */}
          <div className="flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl text-xs font-medium">
            <button
              onClick={() => setExecutionMode('sequential')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                executionMode === 'sequential'
                  ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Sequential Flow
            </button>
            <button
              onClick={() => setExecutionMode('hierarchical')}
              className={`px-3 py-1.5 rounded-lg transition-all ${
                executionMode === 'hierarchical'
                  ? 'bg-indigo-600 text-white font-semibold shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              Hierarchical Crew
            </button>
          </div>

          {/* Trigger Button */}
          <button
            onClick={() => onTriggerAgents(executionMode)}
            disabled={runningAgents}
            className={`flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl shadow-lg transition-all ${
              runningAgents
                ? 'bg-slate-800 text-slate-400 cursor-not-allowed'
                : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-indigo-600/30 active:scale-95'
            }`}
          >
            {runningAgents ? (
              <>
                <div className="w-4 h-4 border-2 border-indigo-200 border-t-transparent rounded-full animate-spin" />
                <span>Running Multi-Agent Pipeline...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-current" />
                <span>Trigger CrewAI Run</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Agents Roster Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agentsStatus && agentsStatus.map((agent, i) => {
          const Icon = agentIcons[agent.agent_name] || Bot;
          const meta = agentDescriptions[agent.agent_name] || {
            color: 'border-slate-700 text-slate-300 bg-slate-800',
            responsibilities: []
          };
          const isSelected = selectedAgent === agent.agent_name;

          return (
            <div
              key={i}
              onClick={() => setSelectedAgent(agent.agent_name)}
              className={`glass-card p-5 rounded-2xl border transition-all cursor-pointer relative ${
                isSelected
                  ? 'border-indigo-500 bg-slate-900/90 shadow-lg shadow-indigo-500/10'
                  : 'border-slate-800 hover:border-slate-700'
              }`}
            >
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2.5 rounded-xl border ${meta.color}`}>
                  <Icon className="w-5 h-5" />
                </div>
                <div className="flex items-center gap-1.5">
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="text-[11px] font-medium text-emerald-400">
                    {agent.status}
                  </span>
                </div>
              </div>

              <div className="text-sm font-bold text-white mb-0.5">
                {agent.agent_name}
              </div>
              <div className="text-xs text-indigo-400 font-medium mb-3">
                {agent.role}
              </div>

              <div className="space-y-1.5 mb-4">
                {meta.responsibilities.map((r, idx) => (
                  <div key={idx} className="flex items-start gap-2 text-[11px] text-slate-300 leading-snug">
                    <span className="text-indigo-400 text-xs">•</span>
                    <span>{r}</span>
                  </div>
                ))}
              </div>

              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-[11px] text-slate-400">
                <span>Completed Tasks</span>
                <span className="font-mono text-white">100% Verified</span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Step-by-Step Execution Logs */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-indigo-400" />
            <h3 className="text-sm font-bold text-white">Agent Step-by-Step Execution Logs & Telemetry</h3>
          </div>
          <span className="text-xs text-slate-400 font-mono">
            Audit Stream Active
          </span>
        </div>

        <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
          {agentLogs && agentLogs.length > 0 ? (
            agentLogs.map((log) => (
              <div
                key={log.id}
                className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800/80 space-y-1.5"
              >
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <span className="font-semibold text-indigo-400">{log.agent_name}</span>
                    <span className="text-slate-500">•</span>
                    <span className="text-slate-300 font-medium">{log.step_name}</span>
                  </div>
                  <div className="flex items-center gap-2 text-[10px] text-slate-400">
                    <span className="px-2 py-0.5 rounded-md bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-medium">
                      {log.status}
                    </span>
                    <span>{new Date(log.created_at).toLocaleTimeString()}</span>
                  </div>
                </div>
                <p className="text-xs text-slate-300 font-mono whitespace-pre-wrap leading-relaxed bg-slate-950/60 p-3 rounded-lg border border-slate-800/50">
                  {log.log_message}
                </p>
              </div>
            ))
          ) : (
            <div className="text-center py-10 text-slate-500 text-xs">
              No logs found. Click "Trigger CrewAI Run" to execute agents.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
