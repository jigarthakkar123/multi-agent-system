import React, { useState } from 'react';
import {
  FileText,
  FileDown,
  ShieldCheck,
  CheckCircle2,
  Calendar,
  Layers,
  Sparkles,
  ExternalLink
} from 'lucide-react';
import { getReportPdfUrl, downloadReportPdfBlob } from '../services/api';

export default function ReportsView({ reports, currentReport, onSelectReport }) {
  const [selectedReportId, setSelectedReportId] = useState(
    currentReport ? currentReport.id : (reports && reports[0] ? reports[0].id : 1)
  );

  const report = currentReport && currentReport.id === selectedReportId
    ? currentReport
    : (reports && reports.find((r) => r.id === selectedReportId)) || currentReport;

  const handleDownloadPdf = async (id) => {
    const targetId = id || selectedReportId;
    try {
      await downloadReportPdfBlob(targetId);
    } catch (e) {
      window.open(getReportPdfUrl(targetId), '_blank');
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <FileText className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-bold text-white">Business Intelligence Reports & Audit Vault</h2>
            <span className="px-2 py-0.5 text-[10px] font-bold uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-md">
              Audit Verified
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Official multi-agent verified intelligence reports. Cross-checked with raw SQLite / PostgreSQL database records.
          </p>
        </div>

        <button
          onClick={() => handleDownloadPdf(report?.id)}
          className="flex items-center gap-2 px-4 py-2 text-xs font-semibold rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/25 active:scale-95 transition-all"
        >
          <FileDown className="w-4 h-4" />
          <span>Download PDF Business Report</span>
        </button>
      </div>

      {/* Main Report View Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Left Column: Reports History List */}
        <div className="glass-card p-4 rounded-2xl border border-slate-800 space-y-2 h-fit">
          <div className="text-xs font-bold text-white uppercase tracking-wider mb-2 px-1">
            Generated Reports
          </div>
          <div className="space-y-1.5">
            {reports && reports.map((r) => (
              <button
                key={r.id}
                onClick={() => {
                  setSelectedReportId(r.id);
                  if (onSelectReport) onSelectReport(r.id);
                }}
                className={`w-full text-left p-3 rounded-xl transition-all text-xs ${
                  selectedReportId === r.id
                    ? 'bg-indigo-600 text-white font-semibold shadow-md'
                    : 'bg-slate-900/60 hover:bg-slate-800 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="font-mono text-[10px] opacity-80">Report #{r.id}</span>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/20 text-emerald-300">
                    {r.confidence_score}%
                  </span>
                </div>
                <div className="truncate font-medium">{r.title}</div>
                <div className="text-[10px] opacity-70 mt-1 flex items-center gap-1">
                  <Calendar className="w-3 h-3" />
                  <span>{new Date(r.created_at).toLocaleDateString()}</span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Right Column: Full Report Document Preview */}
        <div className="lg:col-span-3 glass-card p-6 rounded-2xl border border-slate-800 space-y-6">
          {report ? (
            <>
              {/* Document Header */}
              <div className="pb-4 border-b border-slate-800/80 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-mono text-indigo-400">REPORT #{report.id}</span>
                  <h3 className="text-lg font-bold text-white mt-0.5">{report.title}</h3>
                  <div className="text-xs text-slate-400 mt-1 flex items-center gap-3">
                    <span>Industry: <strong className="text-slate-200">{report.industry}</strong></span>
                    <span>•</span>
                    <span>Coverage: <strong className="text-slate-200">{report.period_start} to {report.period_end}</strong></span>
                  </div>
                </div>

                {/* Audit Stamp */}
                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-emerald-400" />
                  <div>
                    <div className="font-bold text-emerald-300">Audited & Verified</div>
                    <div className="text-[10px] text-emerald-400/80">Confidence: {report.confidence_score}%</div>
                  </div>
                </div>
              </div>

              {/* Executive Summary */}
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                  1. Executive Summary
                </h4>
                <p className="text-xs text-slate-200 leading-relaxed bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
                  {report.summary}
                </p>
              </div>

              {/* Multi-Agent Synthesized Sections */}
              {report.agent_insights_json && (
                <div className="space-y-4">
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    2. Multi-Agent Operational Intelligence Sections
                  </h4>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.entries(report.agent_insights_json).map(([agentKey, text], idx) => (
                      <div key={idx} className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 space-y-2">
                        <div className="text-xs font-bold text-indigo-300 capitalize flex items-center gap-1.5">
                          <span className="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
                          <span>{agentKey.replace('_', ' ')} Agent Findings</span>
                        </div>
                        <p className="text-[11px] text-slate-300 font-mono whitespace-pre-wrap leading-relaxed max-h-48 overflow-y-auto">
                          {text}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Verification Checklist */}
              {report.verification_details_json && report.verification_details_json.verified_facts && (
                <div>
                  <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">
                    3. Zero-Hallucination Evidence Verification Audit
                  </h4>
                  <div className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80 space-y-1.5">
                    {report.verification_details_json.verified_facts.map((fact, idx) => (
                      <div key={idx} className="flex items-center gap-2 text-xs text-emerald-400">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400 flex-shrink-0" />
                        <span className="text-slate-300">{fact}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </>
          ) : (
            <div className="py-20 text-center text-slate-500 text-xs">
              No report available. Click "Trigger CrewAI Run" to generate one.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
