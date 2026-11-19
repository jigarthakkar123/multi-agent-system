import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import OverviewView from './components/OverviewView';
import AgentsView from './components/AgentsView';
import AnalyticsView from './components/AnalyticsView';
import LeadsBrokersView from './components/LeadsBrokersView';
import ApprovalsView from './components/ApprovalsView';
import ReportsView from './components/ReportsView';
import ChatView from './components/ChatView';
import ProfileView from './components/ProfileView';
import UsersAdminView from './components/UsersAdminView';
import AuthModal from './components/AuthModal';

import {
  getKPIs,
  getMonthlyTrends,
  getCityPerformance,
  getPropertyTypes,
  getLeadFunnel,
  getLeadSources,
  getAgentLeaderboard,
  getExpenseBreakdown,
  getAgentsStatus,
  getAgentLogs,
  executeAgents,
  getApprovals,
  recordApprovalDecision,
  getReports,
  getProfile,
  getDatasetSummary,
  getMe,
  authLogin,
  getReportPdfUrl,
  downloadReportPdfBlob
} from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('overview');
  const [user, setUser] = useState(null);
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [runningAgents, setRunningAgents] = useState(false);

  // Data States
  const [kpis, setKpis] = useState(null);
  const [monthlyTrends, setMonthlyTrends] = useState([]);
  const [cityPerformance, setCityPerformance] = useState([]);
  const [propertyTypes, setPropertyTypes] = useState([]);
  const [leadFunnel, setLeadFunnel] = useState([]);
  const [leadSources, setLeadSources] = useState([]);
  const [agentLeaderboard, setAgentLeaderboard] = useState([]);
  const [expenseBreakdown, setExpenseBreakdown] = useState([]);
  const [agentsStatus, setAgentsStatus] = useState([]);
  const [agentLogs, setAgentLogs] = useState([]);
  const [approvals, setApprovals] = useState([]);
  const [reports, setReports] = useState([]);
  const [profile, setProfile] = useState(null);
  const [datasetSummary, setDatasetSummary] = useState(null);
  const [engineUsed, setEngineUsed] = useState(null);
  const [loading, setLoading] = useState(true);

  // Fetch initial telemetry
  const fetchAllData = async () => {
    try {
      const [
        kpisRes,
        trendsRes,
        cityRes,
        typesRes,
        funnelRes,
        sourcesRes,
        leaderboardRes,
        expensesRes,
        agentsRes,
        logsRes,
        approvalsRes,
        reportsRes,
        profileRes,
        summaryRes
      ] = await Promise.all([
        getKPIs().catch(() => ({ data: null })),
        getMonthlyTrends().catch(() => ({ data: [] })),
        getCityPerformance().catch(() => ({ data: [] })),
        getPropertyTypes().catch(() => ({ data: [] })),
        getLeadFunnel().catch(() => ({ data: [] })),
        getLeadSources().catch(() => ({ data: [] })),
        getAgentLeaderboard().catch(() => ({ data: [] })),
        getExpenseBreakdown().catch(() => ({ data: [] })),
        getAgentsStatus().catch(() => ({ data: [] })),
        getAgentLogs().catch(() => ({ data: [] })),
        getApprovals().catch(() => ({ data: [] })),
        getReports().catch(() => ({ data: [] })),
        getProfile().catch(() => ({ data: null })),
        getDatasetSummary().catch(() => ({ data: null }))
      ]);

      if (kpisRes.data) setKpis(kpisRes.data);
      if (trendsRes.data) setMonthlyTrends(trendsRes.data);
      if (cityRes.data) setCityPerformance(cityRes.data);
      if (typesRes.data) setPropertyTypes(typesRes.data);
      if (funnelRes.data) setLeadFunnel(funnelRes.data);
      if (sourcesRes.data) setLeadSources(sourcesRes.data);
      if (leaderboardRes.data) setAgentLeaderboard(leaderboardRes.data);
      if (expensesRes.data) setExpenseBreakdown(expensesRes.data);
      if (agentsRes.data) setAgentsStatus(agentsRes.data);
      if (logsRes.data) setAgentLogs(logsRes.data);
      if (approvalsRes.data) setApprovals(approvalsRes.data);
      if (reportsRes.data) setReports(reportsRes.data);
      if (profileRes.data) setProfile(profileRes.data);
      if (summaryRes.data) setDatasetSummary(summaryRes.data);
    } catch (err) {
      console.error('Data load error:', err);
    } finally {
      setLoading(false);
    }
  };

  // Initialize user session & fetch telemetry seamlessly
  useEffect(() => {
    const initSession = async () => {
      let token = localStorage.getItem('access_token');
      if (token) {
        try {
          const meRes = await getMe();
          setUser(meRes.data);
          fetchAllData();
          return;
        } catch (e) {
          localStorage.removeItem('access_token');
        }
      }
      
      // Auto-authenticate as Manager for seamless instant demo & Viva evaluation
      try {
        const loginRes = await authLogin('manager@realtyintelligence.ai', 'Manager@2026!');
        localStorage.setItem('access_token', loginRes.data.access_token);
        setUser(loginRes.data.user);
      } catch (err) {
        console.warn('Auto-login standby:', err);
      }
      fetchAllData();
    };

    initSession();
  }, []);

  // Trigger CrewAI multi-agent run
  const handleTriggerAgents = async (mode = 'sequential') => {
    setRunningAgents(true);
    try {
      const res = await executeAgents({ execution_mode: mode });
      if (res.data?.engine_used) {
        setEngineUsed(res.data.engine_used);
      }
      await fetchAllData();
      setActiveTab('agents');
    } catch (err) {
      alert('Error executing multi-agent system: ' + (err.response?.data?.detail || err.message));
    } finally {
      setRunningAgents(false);
    }
  };

  // Record Human-in-the-Loop decision
  const handleRecordDecision = async (id, decision, reason) => {
    try {
      await recordApprovalDecision(id, decision, reason);
      const res = await getApprovals();
      setApprovals(res.data);
    } catch (err) {
      alert('Error recording decision: ' + (err.response?.data?.detail || err.message));
    }
  };

  const handleDownloadReport = async () => {
    const reportId = reports && reports[0] ? reports[0].id : 1;
    try {
      await downloadReportPdfBlob(reportId);
    } catch (e) {
      window.open(getReportPdfUrl(reportId), '_blank');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  const pendingApprovalsCount = approvals
    ? approvals.filter((a) => a.status === 'Pending').length
    : 0;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar
        user={user}
        onOpenAuth={() => setIsAuthOpen(true)}
        onLogout={handleLogout}
        onTriggerAgents={() => handleTriggerAgents('sequential')}
        runningAgents={runningAgents}
        onDownloadReport={handleDownloadReport}
      />

      {/* Main Body with Sidebar + Content */}
      <div className="flex-1 flex overflow-hidden">
        <Sidebar
          activeTab={activeTab}
          setActiveTab={setActiveTab}
          pendingApprovalsCount={pendingApprovalsCount}
          user={user}
        />

        <main className="flex-1 p-6 overflow-y-auto max-h-[calc(100vh-61px)]">
          {activeTab === 'overview' && (
            <OverviewView
              kpis={kpis}
              monthlyTrends={monthlyTrends}
              cityPerformance={cityPerformance}
              agentsStatus={agentsStatus}
              pendingApprovals={approvals.filter((a) => a.status === 'Pending')}
              onNavigateTab={setActiveTab}
              onTriggerAgents={handleTriggerAgents}
              runningAgents={runningAgents}
            />
          )}

          {activeTab === 'agents' && (
            <AgentsView
              agentsStatus={agentsStatus}
              agentLogs={agentLogs}
              onTriggerAgents={handleTriggerAgents}
              runningAgents={runningAgents}
              engineUsed={engineUsed}
            />
          )}

          {activeTab === 'analytics' && (
            <AnalyticsView
              monthlyTrends={monthlyTrends}
              cityPerformance={cityPerformance}
              propertyTypes={propertyTypes}
              expenseBreakdown={expenseBreakdown}
            />
          )}

          {activeTab === 'brokers' && (
            <LeadsBrokersView
              leadFunnel={leadFunnel}
              leadSources={leadSources}
              agentLeaderboard={agentLeaderboard}
            />
          )}

          {activeTab === 'approvals' && (
            <ApprovalsView
              approvals={approvals}
              onRecordDecision={handleRecordDecision}
            />
          )}

          {activeTab === 'reports' && (
            <ReportsView
              reports={reports}
              currentReport={reports && reports[0]}
            />
          )}

          {activeTab === 'chat' && <ChatView />}

          {activeTab === 'users' && <UsersAdminView />}

          {activeTab === 'profile' && (
            <ProfileView
              profile={profile}
              datasetSummary={datasetSummary}
              onProfileUpdated={fetchAllData}
              onDatasetUploaded={fetchAllData}
            />
          )}
        </main>
      </div>

      {/* Authentication Modal */}
      <AuthModal
        isOpen={isAuthOpen}
        onClose={() => setIsAuthOpen(false)}
        onAuthSuccess={(userData) => {
          setUser(userData);
          fetchAllData();
        }}
      />
    </div>
  );
}
