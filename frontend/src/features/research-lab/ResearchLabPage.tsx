import React, { useState, useEffect } from 'react';
import {
  FlaskConical,
  Play,
  RotateCcw,
  CheckCircle2,
  Clock,
  AlertTriangle,
  FileText,
  BookOpen,
  Atom,
  ShieldAlert,
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { startResearchRun, getResearchJob, getResearchJobResults } from '../../services/research';
import { getResearchDivisions } from '../../services/projects';
import { ResearchDivision, ResearchJob } from '../../types/research';
import { StructuredReportViewer } from '../../components/reports/StructuredReportViewer';

export const ResearchLabPage: React.FC = () => {
  const [query, setQuery] = useState(
    'Posterior pedicle screw fixation removal criteria and long-term spinal fusion stability in thoracolumbar reconstruction'
  );
  const [divisions, setDivisions] = useState<ResearchDivision[]>([]);
  const [selectedDivision, setSelectedDivision] = useState('arakno-spine');
  const [sources, setSources] = useState<string[]>(['pubmed', 'europe_pmc', 'alphafold']);
  const [maxResults, setMaxResults] = useState(15);
  const [activeJob, setActiveJob] = useState<ResearchJob | null>(null);
  const [jobResults, setJobResults] = useState<any>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    getResearchDivisions().then(setDivisions).catch(console.error);
  }, []);

  // Poll for job completion if active
  useEffect(() => {
    if (!activeJob || activeJob.status === 'completed' || activeJob.status === 'failed') return;

    const interval = setInterval(async () => {
      try {
        const updated = await getResearchJob(activeJob.id);
        setActiveJob(updated);

        if (updated.status === 'completed') {
          const res = await getResearchJobResults(updated.id);
          setJobResults(res.data);
        }
      } catch (err) {
        console.error('Error polling research job status:', err);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [activeJob]);

  const handleStartResearch = async () => {
    if (!query.trim()) return;
    setIsSubmitting(true);
    setJobResults(null);
    try {
      const job = await startResearchRun({
        query,
        division_slug: selectedDivision,
        sources,
        max_results: maxResults,
        synthesize_ai: false, // Local zero-budget rule-based mode default
      });
      setActiveJob(job);
    } catch (e) {
      console.error('Failed to launch research run:', e);
    } finally {
      setIsSubmitting(false);
    }
  };

  const toggleSource = (src: string) => {
    setSources((prev) =>
      prev.includes(src) ? prev.filter((s) => s !== src) : [...prev, src]
    );
  };

  return (
    <div className="space-y-6">
      <div className={jobResults ? "print:hidden space-y-6" : "space-y-6"}>
        <PageHeader
          title="Research lab"
          subtitle="Runs the literature and protein retrieval pipeline against PubMed, Europe PMC, and AlphaFold DB."
          badge="Pipeline"
        />

        {/* Main Research Query Form */}
      <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-5">
        <div>
          <label className="block text-xs font-semibold uppercase tracking-wider text-[#8b949e] mb-2">
            Research question or hypothesis
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            placeholder="Enter an objective biomedical question (e.g. Bone healing dynamics around bioactive cages vs titanium implants)..."
            className="w-full rounded-md bg-[#0f1117] border border-[#30363d] p-3 text-sm text-[#e6edf3] placeholder-gray-500 focus:border-blue-500 focus:outline-none transition"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Research Division */}
          <div>
            <label className="block text-xs font-semibold text-[#8b949e] mb-1.5">Research division</label>
            <select
              value={selectedDivision}
              onChange={(e) => setSelectedDivision(e.target.value)}
              className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3] focus:outline-none"
            >
              {divisions.map((d) => (
                <option key={d.slug} value={d.slug}>
                  {d.name}
                </option>
              ))}
            </select>
          </div>

          {/* Sources Selection */}
          <div>
            <label className="block text-xs font-semibold text-[#8b949e] mb-1.5">Sources</label>
            <div className="flex items-center gap-3 mt-2">
              <label className="flex items-center gap-1.5 text-xs text-gray-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={sources.includes('pubmed')}
                  onChange={() => toggleSource('pubmed')}
                  className="rounded border-gray-700 bg-gray-900 text-blue-500"
                />
                PubMed
              </label>
              <label className="flex items-center gap-1.5 text-xs text-gray-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={sources.includes('europe_pmc')}
                  onChange={() => toggleSource('europe_pmc')}
                  className="rounded border-gray-700 bg-gray-900 text-blue-500"
                />
                Europe PMC
              </label>
              <label className="flex items-center gap-1.5 text-xs text-gray-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={sources.includes('alphafold')}
                  onChange={() => toggleSource('alphafold')}
                  className="rounded border-gray-700 bg-gray-900 text-blue-500"
                />
                AlphaFold DB
              </label>
            </div>
          </div>

          {/* Max Results */}
          <div>
            <label className="block text-xs font-semibold text-[#8b949e] mb-1.5">
              Maximum publications ({maxResults})
            </label>
            <input
              type="range"
              min="5"
              max="50"
              step="5"
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              className="w-full accent-blue-500"
            />
          </div>
        </div>

        <div className="flex items-center justify-between pt-2 border-t border-[#30363d]/50">
          <div className="flex items-center gap-2 text-xs text-amber-400">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Runs locally. Every claim retains its original PMID or DOI.</span>
          </div>
          <button
            onClick={handleStartResearch}
            disabled={isSubmitting || !query.trim()}
            className="flex items-center gap-2 px-5 py-2 rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-bold shadow-md transition"
          >
            <Play className="w-4 h-4 fill-current" />
            {isSubmitting ? 'Starting...' : 'Run research pipeline'}
          </button>
        </div>
      </div>

      {/* Real-time Job Progress Section */}
      {activeJob && (
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="font-semibold text-sm text-[#e6edf3]">Job: {activeJob.id.slice(0, 8)}</span>
              <span
                className={`px-2 py-0.5 rounded text-[11px] font-bold uppercase tracking-wider ${
                  activeJob.status === 'completed'
                    ? 'bg-emerald-950/80 text-emerald-400 border border-emerald-800'
                    : activeJob.status === 'running'
                    ? 'bg-blue-950/80 text-blue-400 border border-blue-800 animate-pulse'
                    : 'bg-gray-800 text-gray-300'
                }`}
              >
                {activeJob.status}
              </span>
            </div>
            <span className="text-xs font-mono text-[#8b949e]">
              Progress: {Math.round(activeJob.progress * 100)}%
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full h-2 rounded-full bg-[#0f1117] overflow-hidden">
            <div
              className="h-full bg-blue-500 transition-all duration-500"
              style={{ width: `${Math.max(activeJob.progress * 100, 5)}%` }}
            />
          </div>

          {/* Pipeline Stages Indicator */}
          <div className="grid grid-cols-2 md:grid-cols-6 gap-2 pt-2 text-[11px]">
            <div className={`p-2 rounded border ${activeJob.progress >= 0.15 ? 'border-blue-700 bg-blue-950/20 text-blue-300' : 'border-gray-800 text-gray-500'}`}>
              1. Query intake
            </div>
            <div className={`p-2 rounded border ${activeJob.progress >= 0.40 ? 'border-blue-700 bg-blue-950/20 text-blue-300' : 'border-gray-800 text-gray-500'}`}>
              2. Literature search
            </div>
            <div className={`p-2 rounded border ${activeJob.progress >= 0.60 ? 'border-blue-700 bg-blue-950/20 text-blue-300' : 'border-gray-800 text-gray-500'}`}>
              3. Protein targets
            </div>
            <div className={`p-2 rounded border ${activeJob.progress >= 0.75 ? 'border-blue-700 bg-blue-950/20 text-blue-300' : 'border-gray-800 text-gray-500'}`}>
              4. Evidence claims
            </div>
            <div className={`p-2 rounded border ${activeJob.progress >= 0.85 ? 'border-blue-700 bg-blue-950/20 text-blue-300' : 'border-gray-800 text-gray-500'}`}>
              5. Citation audit
            </div>
            <div className={`p-2 rounded border ${activeJob.progress >= 1.0 ? 'border-emerald-700 bg-emerald-950/20 text-emerald-300' : 'border-gray-800 text-gray-500'}`}>
              6. Report generated
            </div>
          </div>
        </div>
      )}
      </div>

      {/* Synthesized Research Dossier */}
      {jobResults && (
        <StructuredReportViewer
          title={`Investigation: ${jobResults.query}`}
          content={jobResults.report_markdown}
          status="completed"
          jobResult={jobResults}
        />
      )}
    </div>
  );
};
