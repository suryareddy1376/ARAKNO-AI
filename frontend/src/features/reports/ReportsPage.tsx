import React, { useState, useEffect } from 'react';
import {
  FileText,
  Download,
  Trash2,
  Calendar,
  Clock,
  ExternalLink,
  ShieldCheck,
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { EmptyState } from '../../components/common/EmptyState';
import { getReports, getReport, deleteReport } from '../../services/reports';
import { ResearchReport } from '../../types/reports';
import { useNotificationStore } from '../../stores/notificationStore';
import { StructuredReportViewer } from '../../components/reports/StructuredReportViewer';

export const ReportsPage: React.FC = () => {
  const { addToast } = useNotificationStore();
  const [reports, setReports] = useState<ResearchReport[]>([]);
  const [selectedReport, setSelectedReport] = useState<ResearchReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  const loadReports = async () => {
    setIsLoading(true);
    try {
      const res = await getReports();
      setReports(res);
      if (res.length > 0 && !selectedReport) {
        setSelectedReport(res[0]);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadReports();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      await deleteReport(id);
      addToast({ type: 'info', message: 'Report deleted' });
      if (selectedReport?.id === id) {
        setSelectedReport(null);
      }
      loadReports();
    } catch (e) {
      addToast({ type: 'error', message: 'Failed to delete report' });
    }
  };

  const handleDownload = (report: ResearchReport) => {
    if (!report.content) return;
    const blob = new Blob([report.content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${report.title.slice(0, 30).replace(/\s+/g, '_')}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6 print:space-y-0">
      <div className="print:hidden">
        <PageHeader
          title="Research reports"
          subtitle="Compiled research reports saved locally with citation records."
          badge="Markdown archives"
        />
      </div>

      {isLoading ? (
        <LoadingState message="Loading reports..." />
      ) : reports.length === 0 ? (
        <EmptyState
          icon={FileText}
          title="No research reports"
          description="Reports generated in the research lab are archived here as Markdown files."
        />
      ) : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 print:block">
          {/* Left Column: Report List */}
          <div className="space-y-3 print:hidden">
            <span className="text-xs font-medium uppercase tracking-wider text-[#8b949e] px-1">
              Saved reports ({reports.length})
            </span>
            <div className="space-y-2">
              {reports.map((r) => {
                const isSelected = selectedReport?.id === r.id;
                return (
                  <div
                    key={r.id}
                    onClick={() => setSelectedReport(r)}
                    className={`rounded-lg border p-4 cursor-pointer transition ${
                      isSelected
                        ? 'border-blue-500 bg-[#1c2333] shadow-sm'
                        : 'border-[#30363d] bg-[#161b22] hover:border-gray-600'
                    }`}
                  >
                    <div className="flex items-center justify-between text-[10px] text-gray-400 mb-1">
                      <span className="font-mono uppercase font-semibold text-blue-400">
                        {r.report_type}
                      </span>
                      <span>{new Date(r.created_at).toLocaleDateString()}</span>
                    </div>
                    <h4 className="text-xs font-semibold text-[#e6edf3] line-clamp-2">{r.title}</h4>
                    <span className="text-[11px] text-gray-500 mt-2 block">
                      {r.word_count} words, Markdown
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Right Column: Active Report Viewer */}
          <div className="lg:col-span-2 space-y-4 print:w-full print:space-y-0">
            {selectedReport ? (
              <div className="space-y-4 print:space-y-0">
                <div className="flex justify-end print:hidden">
                  <button
                    onClick={() => handleDelete(selectedReport.id)}
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded hover:bg-rose-950/40 text-gray-400 hover:text-rose-400 border border-transparent hover:border-rose-900/40 text-xs transition"
                    title="Delete report"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                    <span>Delete report</span>
                  </button>
                </div>
                <StructuredReportViewer
                  title={selectedReport.title}
                  content={selectedReport.content || ''}
                  status={selectedReport.status}
                  createdAt={selectedReport.created_at}
                  wordCount={selectedReport.word_count}
                />
              </div>
            ) : (
              <div className="rounded-lg border border-dashed border-[#30363d] bg-[#161b22] p-12 text-center text-xs text-gray-400">
                Select a report to view its contents.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
