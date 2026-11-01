import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  BookOpen,
  Atom,
  FileCheck,
  FolderKanban,
  FileText,
  Activity,
  ArrowRight,
  FlaskConical,
  Search,
  ExternalLink,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  PieChart,
  Pie,
  Cell,
} from 'recharts';

import { PageHeader } from '../../components/common/PageHeader';
import { StatCard } from '../../components/common/StatCard';
import { LoadingState } from '../../components/common/LoadingState';
import { ErrorState } from '../../components/common/ErrorState';
import { getDashboardOverview } from '../../services/dashboard';
import { DashboardOverviewResponse } from '../../types/dashboard';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardOverviewResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const res = await getDashboardOverview();
      setData(res);
    } catch (e: any) {
      setError(e.message || 'Failed to load dashboard overview');
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (isLoading) return <LoadingState message="Loading dashboard data..." />;
  if (error || !data) return <ErrorState title="Dashboard error" message={error || 'No data'} onRetry={loadData} />;

  const stats = data.statistics;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Research lab overview"
        subtitle="Counts from local SQLite database, active projects, and cached structural models."
        badge="Local system"
        actions={
          <button
            onClick={() => navigate('/research-lab')}
            className="flex items-center gap-2 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-md transition"
          >
            <FlaskConical className="w-4 h-4" />
            New research query
          </button>
        }
      />

      {/* Primary Metric Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <StatCard
          title="Saved publications"
          value={stats.total_publications}
          icon={BookOpen}
          color="#3b82f6"
          subtitle="PubMed and Europe PMC"
        />
        <StatCard
          title="Protein records"
          value={stats.total_proteins}
          icon={Atom}
          color="#06b6d4"
          subtitle="UniProt entries"
        />
        <StatCard
          title="3D structures"
          value={stats.total_structures}
          icon={Activity}
          color="#8b5cf6"
          subtitle="AlphaFold PDB files"
        />
        <StatCard
          title="Evidence claims"
          value={stats.total_evidence_records}
          icon={FileCheck}
          color="#10b981"
          subtitle="Categories A to E"
        />
        <StatCard
          title="Active projects"
          value={stats.total_projects}
          icon={FolderKanban}
          color="#f59e0b"
          subtitle="6 divisions"
        />
        <StatCard
          title="Research reports"
          value={stats.total_reports}
          icon={FileText}
          color="#ec4899"
          subtitle="Markdown dossiers"
        />
      </div>

      {/* Quick Action Buttons */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        <button
          onClick={() => navigate('/research-lab')}
          className="flex items-center justify-between p-3 rounded-lg border border-[#30363d] bg-[#161b22] hover:border-blue-500/50 hover:bg-[#1c2333] text-left transition group"
        >
          <div>
            <span className="block text-xs font-semibold text-[#e6edf3]">Start research</span>
            <span className="text-[10px] text-gray-400">Run search pipeline</span>
          </div>
          <ArrowRight className="w-4 h-4 text-blue-400 group-hover:translate-x-0.5 transition" />
        </button>

        <button
          onClick={() => navigate('/literature')}
          className="flex items-center justify-between p-3 rounded-lg border border-[#30363d] bg-[#161b22] hover:border-blue-500/50 hover:bg-[#1c2333] text-left transition group"
        >
          <div>
            <span className="block text-xs font-semibold text-[#e6edf3]">Search PubMed</span>
            <span className="text-[10px] text-gray-400">Find publications</span>
          </div>
          <Search className="w-4 h-4 text-cyan-400 group-hover:translate-x-0.5 transition" />
        </button>

        <button
          onClick={() => navigate('/proteins')}
          className="flex items-center justify-between p-3 rounded-lg border border-[#30363d] bg-[#161b22] hover:border-blue-500/50 hover:bg-[#1c2333] text-left transition group"
        >
          <div>
            <span className="block text-xs font-semibold text-[#e6edf3]">Explore AlphaFold</span>
            <span className="text-[10px] text-gray-400">View 3D coordinates</span>
          </div>
          <Atom className="w-4 h-4 text-purple-400 group-hover:translate-x-0.5 transition" />
        </button>

        <button
          onClick={() => navigate('/evidence')}
          className="flex items-center justify-between p-3 rounded-lg border border-[#30363d] bg-[#161b22] hover:border-blue-500/50 hover:bg-[#1c2333] text-left transition group"
        >
          <div>
            <span className="block text-xs font-semibold text-[#e6edf3]">Evidence library</span>
            <span className="text-[10px] text-gray-400">Traceable claims</span>
          </div>
          <FileCheck className="w-4 h-4 text-emerald-400 group-hover:translate-x-0.5 transition" />
        </button>

        <button
          onClick={() => navigate('/projects')}
          className="flex items-center justify-between p-3 rounded-lg border border-[#30363d] bg-[#161b22] hover:border-blue-500/50 hover:bg-[#1c2333] text-left transition group"
        >
          <div>
            <span className="block text-xs font-semibold text-[#e6edf3]">Manage projects</span>
            <span className="text-[10px] text-gray-400">Divisions and questions</span>
          </div>
          <FolderKanban className="w-4 h-4 text-amber-400 group-hover:translate-x-0.5 transition" />
        </button>
      </div>

      {/* Visualizations & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Research Divisions Card */}
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 flex flex-col">
          <h3 className="text-sm font-semibold text-[#e6edf3] mb-3">Research divisions</h3>
          <div className="space-y-2.5 flex-1 overflow-y-auto">
            {data.division_distribution.map((div) => (
              <div
                key={div.division_slug}
                onClick={() => navigate('/divisions')}
                className="flex items-center justify-between p-2.5 rounded bg-[#0f1117] border border-[#30363d]/50 hover:border-gray-600 cursor-pointer transition"
              >
                <div className="flex items-center gap-2.5">
                  <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: div.color }} />
                  <span className="text-xs font-medium text-[#e6edf3]">{div.division_name}</span>
                </div>
                <span className="text-[11px] text-gray-400">{div.project_count} project(s)</span>
              </div>
            ))}
          </div>
        </div>

        {/* Evidence Distribution Chart */}
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 flex flex-col">
          <h3 className="text-sm font-semibold text-[#e6edf3] mb-1">Evidence strength counts</h3>
          <p className="text-xs text-[#8b949e] mb-4">Saved claims grouped by assessment level</p>
          <div className="h-48 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={data.evidence_distribution}>
                <XAxis dataKey="strength" stroke="#8b949e" fontSize={11} />
                <YAxis stroke="#8b949e" fontSize={11} allowDecimals={false} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#161b22', borderColor: '#30363d', fontSize: '11px' }}
                />
                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Research Activity Log */}
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 flex flex-col">
          <h3 className="text-sm font-semibold text-[#e6edf3] mb-3">Recent activity</h3>
          <div className="space-y-3 flex-1 overflow-y-auto">
            {data.recent_activities.length === 0 ? (
              <div className="text-center py-8 text-xs text-[#8b949e]">
                No recorded actions yet. Search for a paper or download a model to see log entries.
              </div>
            ) : (
              data.recent_activities.map((act) => (
                <div key={act.id} className="text-xs pb-2 border-b border-[#30363d]/40 last:border-0">
                  <span className="font-semibold text-blue-400 uppercase text-[10px] tracking-wider block">
                    {act.activity_type}
                  </span>
                  <p className="text-[#e6edf3] mt-0.5">{act.description}</p>
                  <span className="text-[10px] text-gray-500">{new Date(act.created_at).toLocaleString()}</span>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
