import React, { useState } from 'react';
import { Building, UploadCloud, Database, Save, CheckCircle, AlertCircle, FileSpreadsheet } from 'lucide-react';
import { updateProfile, uploadDatasetFile } from '../services/api';

export default function ProfileView({ profile, datasetSummary, onProfileUpdated, onDatasetUploaded }) {
  const [formData, setFormData] = useState({
    company_name: profile?.company_name || 'Apex Realty Intelligence Corp',
    industry: profile?.industry || 'Real Estate - Property & Sales Intelligence',
    team_size: profile?.team_size || 55,
    business_goals: profile?.business_goals || 'Optimize sales agent conversion velocity, minimize marketing spend leakage, accelerate listing absorption in Western India property hubs, and ensure zero-hallucination executive decision intelligence.'
  });
  const [saving, setSaving] = useState(false);
  const [saveSuccess, setSaveSuccess] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);

  const handleProfileSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateProfile(formData);
      setSaveSuccess(true);
      if (onProfileUpdated) onProfileUpdated();
      setTimeout(() => setSaveSuccess(false), 3000);
    } catch (err) {
      alert('Failed to update business profile');
    } finally {
      setSaving(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const data = new FormData();
    data.append('file', file);
    setUploading(true);
    setUploadMessage(null);

    try {
      const res = await uploadDatasetFile(data);
      setUploadMessage({ type: 'success', text: res.data.message || 'Dataset uploaded and processed successfully!' });
      if (onDatasetUploaded) onDatasetUploaded();
    } catch (err) {
      setUploadMessage({ type: 'error', text: err.response?.data?.detail || 'Error uploading dataset.' });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Top Banner */}
      <div className="glass-card p-5 rounded-2xl border border-slate-800">
        <h2 className="text-base font-bold text-white mb-1">Business Profile & Dataset Management</h2>
        <p className="text-xs text-slate-400">
          Configure enterprise organizational parameters and manage underlying real estate database telemetry.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Business Profile Form */}
        <div className="glass-card p-5 rounded-2xl border border-slate-800">
          <div className="flex items-center gap-2 mb-4">
            <Building className="w-5 h-5 text-indigo-400" />
            <h3 className="text-sm font-bold text-white">Company Profile Settings</h3>
          </div>

          <form onSubmit={handleProfileSubmit} className="space-y-4 text-xs">
            <div>
              <label className="block text-slate-300 font-medium mb-1">Company / Agency Name</label>
              <input
                type="text"
                value={formData.company_name}
                onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                className="w-full px-3.5 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Industry Vertical</label>
              <input
                type="text"
                value={formData.industry}
                disabled
                className="w-full px-3.5 py-2 bg-slate-950 border border-slate-800 rounded-xl text-slate-400 cursor-not-allowed"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Active Sales Brokers / Team Size</label>
              <input
                type="number"
                value={formData.team_size}
                onChange={(e) => setFormData({ ...formData, team_size: parseInt(e.target.value) || 0 })}
                className="w-full px-3.5 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            <div>
              <label className="block text-slate-300 font-medium mb-1">Core Business & Operations Goals</label>
              <textarea
                rows={4}
                value={formData.business_goals}
                onChange={(e) => setFormData({ ...formData, business_goals: e.target.value })}
                className="w-full px-3.5 py-2 bg-slate-900 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500"
              />
            </div>

            <button
              type="submit"
              disabled={saving}
              className="flex items-center justify-center gap-2 w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl transition-all shadow-md active:scale-95 disabled:bg-slate-800"
            >
              <Save className="w-4 h-4" />
              <span>{saving ? 'Saving...' : 'Save Profile Changes'}</span>
            </button>

            {saveSuccess && (
              <div className="flex items-center gap-1.5 text-emerald-400 text-xs justify-center pt-1">
                <CheckCircle className="w-4 h-4" />
                <span>Profile updated successfully!</span>
              </div>
            )}
          </form>
        </div>

        {/* Dataset Upload & Summary */}
        <div className="space-y-6">
          {/* Summary Box */}
          <div className="glass-card p-5 rounded-2xl border border-slate-800">
            <div className="flex items-center gap-2 mb-3">
              <Database className="w-5 h-5 text-emerald-400" />
              <h3 className="text-sm font-bold text-white">Active Database Inventory</h3>
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs mb-4">
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="text-slate-400 text-[10px]">Total Properties</div>
                <div className="text-base font-bold text-white font-mono mt-0.5">
                  {datasetSummary?.total_properties || 1200}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="text-slate-400 text-[10px]">Customer Leads</div>
                <div className="text-base font-bold text-white font-mono mt-0.5">
                  {datasetSummary?.total_leads || 1800}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="text-slate-400 text-[10px]">Site Visits Conducted</div>
                <div className="text-base font-bold text-white font-mono mt-0.5">
                  {datasetSummary?.total_visits || 1200}
                </div>
              </div>
              <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800">
                <div className="text-slate-400 text-[10px]">Deals Negotiated</div>
                <div className="text-base font-bold text-white font-mono mt-0.5">
                  {datasetSummary?.total_deals || 600}
                </div>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 flex items-center justify-between pt-2 border-t border-slate-800">
              <span>Coverage Period:</span>
              <span className="font-semibold text-slate-200">May 1, 2026 – Oct 31, 2026</span>
            </div>
          </div>

          {/* Dataset Upload Form */}
          <div className="glass-card p-5 rounded-2xl border border-slate-800">
            <div className="flex items-center gap-2 mb-2">
              <UploadCloud className="w-5 h-5 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">Update / Replace Dataset</h3>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Upload an updated multi-sheet Excel file (.xlsx) or CSV containing real estate transactions.
            </p>

            <label className="border-2 border-dashed border-slate-800 hover:border-indigo-500/60 rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer transition-colors bg-slate-950/40">
              <FileSpreadsheet className="w-8 h-8 text-indigo-400 mb-2" />
              <span className="text-xs font-semibold text-slate-200 mb-0.5">
                {uploading ? 'Processing & Re-indexing...' : 'Click to select Excel (.xlsx) file'}
              </span>
              <span className="text-[10px] text-slate-500">Supports multi-sheet real estate workbooks</span>
              <input
                type="file"
                accept=".xlsx,.xls,.csv"
                onChange={handleFileUpload}
                disabled={uploading}
                className="hidden"
              />
            </label>

            {uploadMessage && (
              <div
                className={`mt-3 p-3 rounded-xl text-xs flex items-center gap-2 ${
                  uploadMessage.type === 'success'
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                    : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                }`}
              >
                {uploadMessage.type === 'success' ? <CheckCircle className="w-4 h-4" /> : <AlertCircle className="w-4 h-4" />}
                <span>{uploadMessage.text}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
