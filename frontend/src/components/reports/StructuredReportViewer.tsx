import React, { useState, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import {
  FileText,
  Copy,
  Download,
  Printer,
  CheckCircle2,
  AlertTriangle,
  ExternalLink,
  Layers,
  Dna,
  ShieldCheck,
  Search,
  Filter,
  BookOpen,
  Atom,
  Clock,
  Sparkles,
  ArrowRight,
  ChevronDown,
  Check,
} from 'lucide-react';

import { parseMarkdownReport, ParsedReportData, ParsedEvidence } from '../../utils/reportParser';
import { useNotificationStore } from '../../stores/notificationStore';

interface StructuredReportViewerProps {
  title?: string;
  content?: string;
  status?: string;
  createdAt?: string;
  wordCount?: number;
  jobResult?: any;
  className?: string;
}

const CATEGORY_STYLES: Record<string, { label: string; bg: string; text: string; dot: string }> = {
  A: { label: 'Human clinical', bg: 'bg-emerald-950/60 border-emerald-800/60', text: 'text-emerald-300', dot: 'bg-emerald-400' },
  B: { label: 'Animal experimental', bg: 'bg-amber-950/60 border-amber-800/60', text: 'text-amber-300', dot: 'bg-amber-400' },
  C: { label: 'Cell and laboratory', bg: 'bg-blue-950/60 border-blue-800/60', text: 'text-blue-300', dot: 'bg-blue-400' },
  D: { label: 'Computational predictions', bg: 'bg-purple-950/60 border-purple-800/60', text: 'text-purple-300', dot: 'bg-purple-400' },
  E: { label: 'Theoretical hypotheses', bg: 'bg-pink-950/60 border-pink-800/60', text: 'text-pink-300', dot: 'bg-pink-400' },
};

export const StructuredReportViewer: React.FC<StructuredReportViewerProps> = ({
  title,
  content = '',
  status = 'completed',
  createdAt,
  wordCount,
  jobResult,
  className = '',
}) => {
  const navigate = useNavigate();
  const { addToast } = useNotificationStore();
  const [viewMode, setViewMode] = useState<'structured' | 'publication' | 'raw'>('structured');
  const [activeTab, setActiveTab] = useState<'summary' | 'targets' | 'evidence' | 'references' | 'verification' | 'synthesis'>('summary');

  // Evidence filters
  const [evidenceFilter, setEvidenceFilter] = useState<string>('all');
  const [evidenceSearch, setEvidenceSearch] = useState<string>('');
  const [copied, setCopied] = useState(false);

  // Parse markdown if raw string is provided
  const parsedData: ParsedReportData = useMemo(() => {
    return parseMarkdownReport(content, title || 'Research Report');
  }, [content, title]);

  // Merge direct jobResult structured data if available
  const reportTitle = title || parsedData.title;
  const executionSummary = jobResult?.executive_summary || parsedData.executiveSummary;
  const targets = jobResult?.proteins?.length > 0
    ? jobResult.proteins.map((p: any) => ({
        symbol: p.gene_symbol || p.symbol || 'Target',
        name: p.protein_name || p.name || 'Macromolecule',
        accession: p.accession || 'N/A',
        organism: p.organism || 'Homo sapiens',
        plddt: p.alphafold_plddt || p.plddt,
      }))
    : parsedData.targets;

  const rawEvidence = jobResult?.evidence_records?.length > 0
    ? jobResult.evidence_records.map((e: any) => ({
        sourceTitle: e.publication_title || e.title || e.sourceTitle || 'Source Publication',
        sourceUrl: e.url || (e.pmid ? `https://pubmed.ncbi.nlm.nih.gov/${e.pmid}/` : undefined),
        pmid: e.pmid,
        doi: e.doi,
        year: e.year,
        journal: e.journal,
        category: e.evidence_category || e.category || 'C',
        strength: e.strength || 'moderate',
        finding: e.excerpt || e.finding || e.claim || '',
      }))
    : parsedData.evidence;

  const references = jobResult?.publications?.length > 0
    ? jobResult.publications.map((p: any, idx: number) => ({
        index: idx + 1,
        title: p.title,
        authors: Array.isArray(p.authors) ? p.authors.join(', ') : p.authors,
        journal: p.journal,
        year: p.year,
        pmid: p.pmid,
        doi: p.doi,
      }))
    : parsedData.references;

  const verificationStatus = jobResult?.citations_verified !== undefined
    ? (jobResult.citations_verified ? 'VERIFIED' : 'PARTIAL')
    : parsedData.verificationStatus;

  const verificationSummary = jobResult?.verification_summary || parsedData.verificationSummary;
  const aiSynthesis = parsedData.aiSynthesis;

  // Filtered evidence claims
  const filteredEvidence = useMemo(() => {
    return rawEvidence.filter((item: ParsedEvidence) => {
      const matchCat = evidenceFilter === 'all' || item.category.toUpperCase() === evidenceFilter.toUpperCase();
      const matchQuery =
        !evidenceSearch.trim() ||
        item.finding.toLowerCase().includes(evidenceSearch.toLowerCase()) ||
        item.sourceTitle.toLowerCase().includes(evidenceSearch.toLowerCase()) ||
        (item.pmid && item.pmid.includes(evidenceSearch));
      return matchCat && matchQuery;
    });
  }, [rawEvidence, evidenceFilter, evidenceSearch]);

  const handleCopyMarkdown = () => {
    navigator.clipboard.writeText(content);
    setCopied(true);
    addToast({ type: 'success', message: 'Report markdown copied to clipboard' });
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${reportTitle.slice(0, 30).replace(/\s+/g, '_')}_dossier.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Dossier Header & Meta Bar */}
      <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 border-b border-[#30363d]/60 pb-5">
          <div className="space-y-2 max-w-3xl">
            <div className="flex items-center gap-2 flex-wrap text-[11px]">
              <span className="font-mono uppercase font-semibold px-2 py-0.5 rounded bg-blue-950/80 text-blue-300 border border-blue-800/50">
                Scientific intelligence dossier
              </span>
              <span className={`px-2 py-0.5 rounded font-medium uppercase tracking-wider ${
                status === 'completed'
                  ? 'bg-emerald-950/70 text-emerald-300 border border-emerald-800/50'
                  : 'bg-amber-950/70 text-amber-300 border border-amber-800/50'
              }`}>
                {status}
              </span>
              <span className="px-2 py-0.5 rounded bg-emerald-950/70 text-emerald-300 border border-emerald-800/50 flex items-center gap-1 font-medium">
                <ShieldCheck className="w-3.5 h-3.5" />
                {verificationStatus}
              </span>
            </div>

            <h1 className="text-xl md:text-2xl font-bold tracking-tight text-[#e6edf3] leading-snug">
              {reportTitle}
            </h1>

            <div className="flex items-center gap-3 text-xs text-[#8b949e] flex-wrap">
              {createdAt && (
                <span className="flex items-center gap-1">
                  <Clock className="w-3.5 h-3.5" />
                  {new Date(createdAt).toLocaleString()}
                </span>
              )}
              {wordCount && <span>{wordCount.toLocaleString()} words</span>}
              <span>Format: Markdown</span>
            </div>
          </div>

          {/* Quick Actions Toolbar */}
          <div className="flex items-center gap-2 shrink-0">
            <button
              onClick={handleCopyMarkdown}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#0f1117] border border-[#30363d] hover:border-gray-500 text-xs font-medium text-gray-200 transition"
              title="Copy markdown text"
            >
              {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
              <span>{copied ? 'Copied' : 'Copy'}</span>
            </button>
            <button
              onClick={handleDownload}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#0f1117] border border-[#30363d] hover:border-gray-500 text-xs font-medium text-gray-200 transition"
              title="Export as markdown file"
            >
              <Download className="w-3.5 h-3.5" />
              <span>Export</span>
            </button>
            <button
              onClick={handlePrint}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white transition shadow-sm"
              title="Print document"
            >
              <Printer className="w-3.5 h-3.5" />
              <span>Print</span>
            </button>
          </div>
        </div>

        {/* View Mode Switcher */}
        <div className="flex items-center justify-between pt-1">
          <div className="flex rounded-md bg-[#0f1117] border border-[#30363d] p-1 text-xs">
            <button
              onClick={() => setViewMode('structured')}
              className={`px-3 py-1 rounded font-medium transition ${
                viewMode === 'structured'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Structured sections
            </button>
            <button
              onClick={() => setViewMode('publication')}
              className={`px-3 py-1 rounded font-medium transition ${
                viewMode === 'publication'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Publication view
            </button>
            <button
              onClick={() => setViewMode('raw')}
              className={`px-3 py-1 rounded font-medium transition ${
                viewMode === 'raw'
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-gray-400 hover:text-white'
              }`}
            >
              Raw markdown
            </button>
          </div>

          <span className="text-xs text-gray-400 hidden sm:inline">
            Notice: Computational literature analysis for research purposes.
          </span>
        </div>
      </div>

      {/* VIEW MODE 1: STRUCTURED SECTIONS */}
      {viewMode === 'structured' && (
        <div className="space-y-6">
          {/* Executive Stat Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-[#8b949e] font-medium block">Publications</span>
                <span className="text-2xl font-bold text-blue-400 font-mono mt-0.5 block">
                  {references.length || parsedData.publicationCount || 0}
                </span>
                <span className="text-[10px] text-gray-500">Peer-reviewed sources</span>
              </div>
              <div className="w-9 h-9 rounded-md bg-blue-950/60 border border-blue-800/40 flex items-center justify-center text-blue-400">
                <BookOpen className="w-4 h-4" />
              </div>
            </div>

            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-[#8b949e] font-medium block">Evidence claims</span>
                <span className="text-2xl font-bold text-emerald-400 font-mono mt-0.5 block">
                  {rawEvidence.length || parsedData.evidenceCount || 0}
                </span>
                <span className="text-[10px] text-gray-500">Traceable findings</span>
              </div>
              <div className="w-9 h-9 rounded-md bg-emerald-950/60 border border-emerald-800/40 flex items-center justify-center text-emerald-400">
                <FileText className="w-4 h-4" />
              </div>
            </div>

            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-[#8b949e] font-medium block">Biological targets</span>
                <span className="text-2xl font-bold text-purple-400 font-mono mt-0.5 block">
                  {targets.length || parsedData.targetsCount || 0}
                </span>
                <span className="text-[10px] text-gray-500">UniProt / AlphaFold</span>
              </div>
              <div className="w-9 h-9 rounded-md bg-purple-950/60 border border-purple-800/40 flex items-center justify-center text-purple-400">
                <Dna className="w-4 h-4" />
              </div>
            </div>

            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex items-center justify-between">
              <div>
                <span className="text-[11px] text-[#8b949e] font-medium block">Citation verification</span>
                <span className="text-2xl font-bold text-cyan-400 font-mono mt-0.5 block">
                  {verificationStatus === 'VERIFIED' ? '100%' : 'Partial'}
                </span>
                <span className="text-[10px] text-gray-500">PubMed &amp; Europe PMC</span>
              </div>
              <div className="w-9 h-9 rounded-md bg-cyan-950/60 border border-cyan-800/40 flex items-center justify-center text-cyan-400">
                <ShieldCheck className="w-4 h-4" />
              </div>
            </div>
          </div>

          {/* Section Navigation Tabs */}
          <div className="flex items-center gap-1 overflow-x-auto pb-1 border-b border-[#30363d] text-xs">
            <button
              onClick={() => setActiveTab('summary')}
              className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap ${
                activeTab === 'summary'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              1. Executive summary
            </button>
            <button
              onClick={() => setActiveTab('targets')}
              className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap ${
                activeTab === 'targets'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              2. Biological targets ({targets.length})
            </button>
            <button
              onClick={() => setActiveTab('evidence')}
              className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap ${
                activeTab === 'evidence'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              3. Evidence matrix ({rawEvidence.length})
            </button>
            <button
              onClick={() => setActiveTab('references')}
              className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap ${
                activeTab === 'references'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              4. References ({references.length})
            </button>
            <button
              onClick={() => setActiveTab('verification')}
              className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap ${
                activeTab === 'verification'
                  ? 'border-blue-500 text-blue-400'
                  : 'border-transparent text-gray-400 hover:text-white'
              }`}
            >
              5. Citation audit
            </button>
            {aiSynthesis && (
              <button
                onClick={() => setActiveTab('synthesis')}
                className={`px-4 py-2 border-b-2 font-medium transition whitespace-nowrap flex items-center gap-1 ${
                  activeTab === 'synthesis'
                    ? 'border-blue-500 text-blue-400'
                    : 'border-transparent text-gray-400 hover:text-white'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5 text-blue-400" />
                6. AI evidence synthesis
              </button>
            )}
          </div>

          {/* TAB 1: EXECUTIVE SUMMARY */}
          {activeTab === 'summary' && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-5">
              <div className="flex items-center justify-between border-b border-[#30363d]/60 pb-3">
                <h3 className="text-sm font-semibold text-[#e6edf3]">Executive summary</h3>
                <span className="text-[11px] text-gray-400 font-mono">Dossier summary</span>
              </div>

              <div className="p-4 rounded-md bg-[#0f1117] border border-[#30363d] space-y-3">
                <p className="text-sm text-gray-200 leading-relaxed font-sans">
                  {executionSummary || 'This investigation retrieved peer-reviewed scientific literature and macromolecular structure records.'}
                </p>

                <div className="p-3 rounded bg-blue-950/20 border border-blue-900/40 text-xs text-blue-300/90 leading-relaxed">
                  <strong>Research note:</strong> Findings are consolidated from primary databases (PubMed, Europe PMC, UniProt, AlphaFold DB) and classified into evidence hierarchy levels A through E.
                </div>
              </div>
            </div>
          )}

          {/* TAB 2: BIOLOGICAL TARGETS */}
          {activeTab === 'targets' && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[#30363d]/60 pb-3">
                <div>
                  <h3 className="text-sm font-semibold text-[#e6edf3]">Identified biological targets</h3>
                  <p className="text-xs text-[#8b949e]">Macromolecules identified in peer-reviewed literature for this topic</p>
                </div>
                <span className="text-xs font-mono text-purple-400">{targets.length} targets</span>
              </div>

              {targets.length === 0 ? (
                <div className="p-8 text-center text-xs text-gray-400 rounded bg-[#0f1117] border border-[#30363d]/60">
                  No specific protein accession isolated for this query query.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {targets.map((t: any, idx: number) => (
                    <div
                      key={t.accession || idx}
                      className="rounded-lg border border-[#30363d] bg-[#0f1117] p-5 space-y-3 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <span className="px-2 py-0.5 rounded font-mono font-bold text-xs bg-purple-950/70 text-purple-300 border border-purple-800/40">
                              {t.symbol}
                            </span>
                            <h4 className="text-sm font-semibold text-[#e6edf3] mt-2">{t.name}</h4>
                            <p className="text-xs text-[#8b949e] italic mt-0.5">{t.organism}</p>
                          </div>
                          <span className="font-mono text-xs text-gray-400 bg-[#161b22] px-2 py-1 rounded border border-[#30363d]">
                            {t.accession}
                          </span>
                        </div>

                        {t.plddt && (
                          <div className="mt-3 pt-3 border-t border-[#30363d]/40 flex items-center justify-between text-xs">
                            <span className="text-gray-400">AlphaFold mean pLDDT:</span>
                            <span className="font-mono font-bold text-blue-400">{t.plddt}</span>
                          </div>
                        )}
                      </div>

                      <div className="pt-3 border-t border-[#30363d]/40 flex justify-end">
                        <button
                          onClick={() => navigate(`/proteins`)}
                          className="flex items-center gap-1.5 text-xs font-medium text-blue-400 hover:text-blue-300 transition"
                        >
                          <Atom className="w-3.5 h-3.5" />
                          <span>View in 3D viewer</span>
                          <ArrowRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 3: EVIDENCE MATRIX */}
          {activeTab === 'evidence' && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-[#30363d]/60 pb-4">
                <div>
                  <h3 className="text-sm font-semibold text-[#e6edf3]">Evidence matrix</h3>
                  <p className="text-xs text-[#8b949e]">
                    Claims classified across categories A through E ({filteredEvidence.length} displayed)
                  </p>
                </div>

                {/* Filter and Search */}
                <div className="flex items-center gap-2">
                  <div className="relative w-48">
                    <Search className="w-3.5 h-3.5 absolute left-2.5 top-1/2 -translate-y-1/2 text-gray-400" />
                    <input
                      type="text"
                      value={evidenceSearch}
                      onChange={(e) => setEvidenceSearch(e.target.value)}
                      placeholder="Search claims..."
                      className="w-full bg-[#0f1117] border border-[#30363d] rounded pl-8 pr-2.5 py-1 text-xs text-[#e6edf3] focus:outline-none"
                    />
                  </div>

                  <select
                    value={evidenceFilter}
                    onChange={(e) => setEvidenceFilter(e.target.value)}
                    className="bg-[#0f1117] border border-[#30363d] rounded px-2.5 py-1 text-xs text-[#e6edf3] focus:outline-none"
                  >
                    <option value="all">All categories</option>
                    <option value="A">Cat A: Clinical</option>
                    <option value="B">Cat B: Animal</option>
                    <option value="C">Cat C: Cell/Lab</option>
                    <option value="D">Cat D: Computational</option>
                    <option value="E">Cat E: Theoretical</option>
                  </select>
                </div>
              </div>

              {filteredEvidence.length === 0 ? (
                <div className="p-8 text-center text-xs text-gray-400 rounded bg-[#0f1117] border border-[#30363d]/60">
                  No evidence claims match the selected filter.
                </div>
              ) : (
                <div className="overflow-x-auto rounded-lg border border-[#30363d]">
                  <table className="w-full text-left text-xs border-collapse">
                    <thead className="bg-[#0f1117] text-[#8b949e] border-b border-[#30363d]">
                      <tr>
                        <th className="p-3 font-semibold uppercase tracking-wider text-[10px]">Category</th>
                        <th className="p-3 font-semibold uppercase tracking-wider text-[10px]">Strength</th>
                        <th className="p-3 font-semibold uppercase tracking-wider text-[10px]">Source publication</th>
                        <th className="p-3 font-semibold uppercase tracking-wider text-[10px]">Year / Journal</th>
                        <th className="p-3 font-semibold uppercase tracking-wider text-[10px]">Key finding</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-[#30363d]/50 bg-[#161b22]">
                      {filteredEvidence.map((ev: ParsedEvidence, idx: number) => {
                        const catStyle = CATEGORY_STYLES[ev.category.toUpperCase()] || CATEGORY_STYLES['C'];
                        return (
                          <tr key={idx} className="hover:bg-[#1a202c] transition">
                            <td className="p-3 whitespace-nowrap">
                              <span className={`inline-flex items-center gap-1.5 px-2 py-0.5 rounded text-[10px] font-semibold border ${catStyle.bg} ${catStyle.text}`}>
                                <span className={`w-1.5 h-1.5 rounded-full ${catStyle.dot}`} />
                                Cat {ev.category}
                              </span>
                            </td>
                            <td className="p-3 whitespace-nowrap">
                              <span className="px-2 py-0.5 rounded text-[10px] uppercase font-mono bg-gray-800 text-gray-300">
                                {ev.strength}
                              </span>
                            </td>
                            <td className="p-3 max-w-xs">
                              {ev.sourceUrl ? (
                                <a
                                  href={ev.sourceUrl}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="font-medium text-blue-400 hover:text-blue-300 inline-flex items-center gap-1"
                                >
                                  <span className="line-clamp-2">{ev.sourceTitle}</span>
                                  <ExternalLink className="w-3 h-3 shrink-0" />
                                </a>
                              ) : (
                                <span className="font-medium text-gray-200 line-clamp-2">{ev.sourceTitle}</span>
                              )}
                              {ev.pmid && (
                                <span className="text-[10px] font-mono text-gray-500 block mt-0.5">
                                  PMID: {ev.pmid}
                                </span>
                              )}
                            </td>
                            <td className="p-3 whitespace-nowrap text-gray-400">
                              <div>{ev.year || 'N/A'}</div>
                              <div className="text-[11px] text-gray-500 italic max-w-[120px] truncate">{ev.journal}</div>
                            </td>
                            <td className="p-3 text-gray-300 leading-relaxed max-w-md">
                              <p className="line-clamp-3 hover:line-clamp-none transition-all">
                                {ev.finding}
                              </p>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          )}

          {/* TAB 4: PEER-REVIEWED REFERENCES */}
          {activeTab === 'references' && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[#30363d]/60 pb-3">
                <div>
                  <h3 className="text-sm font-semibold text-[#e6edf3]">Peer-reviewed references</h3>
                  <p className="text-xs text-[#8b949e]">Primary publications indexed with verified PMIDs or DOIs</p>
                </div>
                <span className="text-xs font-mono text-blue-400">{references.length} papers</span>
              </div>

              {references.length === 0 ? (
                <div className="p-8 text-center text-xs text-gray-400 rounded bg-[#0f1117] border border-[#30363d]/60">
                  No references parsed for this report.
                </div>
              ) : (
                <div className="space-y-3">
                  {references.map((ref: any) => (
                    <div
                      key={ref.index || ref.pmid || ref.title}
                      className="p-4 rounded-lg border border-[#30363d] bg-[#0f1117] space-y-2"
                    >
                      <div className="flex items-start gap-3">
                        <span className="w-6 h-6 rounded bg-blue-950/80 border border-blue-800/40 text-blue-300 text-xs font-mono font-bold flex items-center justify-center shrink-0">
                          {ref.index}
                        </span>
                        <div className="flex-1 space-y-1">
                          <h4 className="text-xs font-semibold text-[#e6edf3] leading-snug">
                            {ref.title}
                          </h4>
                          {ref.authors && (
                            <p className="text-[11px] text-[#8b949e]">{ref.authors}</p>
                          )}
                          <div className="flex items-center gap-2 text-[11px] text-gray-400">
                            {ref.journal && <span className="italic">{ref.journal}</span>}
                            {ref.year && <span>({ref.year})</span>}
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center justify-between pt-2 border-t border-[#30363d]/40 text-xs">
                        <div className="flex items-center gap-3">
                          {ref.pmid && (
                            <a
                              href={`https://pubmed.ncbi.nlm.nih.gov/${ref.pmid}/`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-blue-400 hover:text-blue-300 font-mono text-[11px] flex items-center gap-1"
                            >
                              <span>PMID: {ref.pmid}</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                          {ref.doi && (
                            <a
                              href={`https://doi.org/${ref.doi}`}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-gray-400 hover:text-gray-200 font-mono text-[11px] flex items-center gap-1"
                            >
                              <span>DOI: {ref.doi}</span>
                              <ExternalLink className="w-3 h-3" />
                            </a>
                          )}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* TAB 5: CITATION AUDIT */}
          {activeTab === 'verification' && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[#30363d]/60 pb-3">
                <h3 className="text-sm font-semibold text-[#e6edf3]">Citation and traceability audit</h3>
                <span className="px-2 py-0.5 rounded text-xs font-medium bg-emerald-950/60 border border-emerald-800 text-emerald-300">
                  {verificationStatus}
                </span>
              </div>

              <div className="p-4 rounded-md bg-[#0f1117] border border-[#30363d] space-y-3">
                <div className="flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  <span className="text-xs font-semibold text-gray-200">{verificationSummary}</span>
                </div>
                <p className="text-xs text-gray-400 leading-relaxed">
                  Every evidence claim synthesized in this report is mapped to verified PubMed Identifier (PMID) or Digital Object Identifier (DOI) records. Fabricated citations, hallucinated authors, or unverified secondary interpretations are prohibited by the pipeline audit node.
                </p>
              </div>
            </div>
          )}

          {/* TAB 6: AI EVIDENCE SYNTHESIS */}
          {activeTab === 'synthesis' && aiSynthesis && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4">
              <div className="flex items-center justify-between border-b border-[#30363d]/60 pb-3">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-blue-400" />
                  <h3 className="text-sm font-semibold text-[#e6edf3]">AI evidence synthesis</h3>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-800/40">
                  Nemotron / Neural analysis
                </span>
              </div>

              <div className="p-4 rounded-md bg-[#0f1117] border border-[#30363d] space-y-3">
                <div className="text-xs text-gray-200 leading-relaxed whitespace-pre-wrap font-sans">
                  {aiSynthesis}
                </div>
                <div className="pt-3 border-t border-[#30363d]/40 text-[11px] text-gray-500 italic">
                  Computational interpretation generated from the structured evidence matrix. Not intended as medical diagnosis or treatment advice.
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* VIEW MODE 2: PUBLICATION VIEW (CONTINUOUS SCIENTIFIC ARTICLE WITH REMARK-GFM) */}
      {viewMode === 'publication' && (
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-8 space-y-6">
          <div className="prose prose-invert max-w-none text-xs leading-relaxed">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              components={{
                h1: ({ node, ...props }) => (
                  <h1 className="text-xl font-bold text-[#e6edf3] border-b border-[#30363d] pb-2 mt-6 mb-3" {...props} />
                ),
                h2: ({ node, ...props }) => (
                  <h2 className="text-base font-semibold text-[#e6edf3] border-b border-[#30363d]/50 pb-1.5 mt-6 mb-3" {...props} />
                ),
                h3: ({ node, ...props }) => (
                  <h3 className="text-sm font-semibold text-blue-400 mt-4 mb-2" {...props} />
                ),
                p: ({ node, ...props }) => (
                  <p className="text-xs text-gray-300 leading-relaxed mb-3" {...props} />
                ),
                table: ({ node, ...props }) => (
                  <div className="overflow-x-auto my-5 rounded-lg border border-[#30363d]">
                    <table className="w-full text-left text-xs border-collapse" {...props} />
                  </div>
                ),
                thead: ({ node, ...props }) => (
                  <thead className="bg-[#0f1117] text-[#8b949e] border-b border-[#30363d]" {...props} />
                ),
                th: ({ node, ...props }) => (
                  <th className="p-2.5 font-semibold uppercase tracking-wider text-[10px]" {...props} />
                ),
                td: ({ node, ...props }) => (
                  <td className="p-2.5 border-b border-[#30363d]/40 text-[#e6edf3] text-xs" {...props} />
                ),
                blockquote: ({ node, ...props }) => (
                  <blockquote className="border-l-4 border-blue-500 bg-blue-950/20 p-3 rounded-r my-4 text-xs text-blue-200" {...props} />
                ),
                ul: ({ node, ...props }) => (
                  <ul className="list-disc pl-5 my-2 space-y-1 text-xs text-gray-300" {...props} />
                ),
                ol: ({ node, ...props }) => (
                  <ol className="list-decimal pl-5 my-2 space-y-1 text-xs text-gray-300" {...props} />
                ),
                li: ({ node, ...props }) => (
                  <li className="text-xs text-gray-300" {...props} />
                ),
                a: ({ node, ...props }) => (
                  <a className="text-blue-400 hover:text-blue-300 underline underline-offset-2" target="_blank" rel="noopener noreferrer" {...props} />
                ),
                code: ({ node, ...props }) => (
                  <code className="font-mono text-[11px] px-1 py-0.5 rounded bg-[#0f1117] text-blue-300 border border-[#30363d]" {...props} />
                ),
              }}
            >
              {content || 'No report markdown available.'}
            </ReactMarkdown>
          </div>
        </div>
      )}

      {/* VIEW MODE 3: RAW MARKDOWN */}
      {viewMode === 'raw' && (
        <div className="rounded-lg border border-[#30363d] bg-[#0f1117] p-5">
          <div className="flex items-center justify-between pb-3 border-b border-[#30363d] text-xs text-[#8b949e] mb-4">
            <span className="font-mono">Raw Markdown Content</span>
            <button
              onClick={handleCopyMarkdown}
              className="flex items-center gap-1 text-blue-400 hover:text-blue-300 transition"
            >
              <Copy className="w-3.5 h-3.5" />
              <span>Copy all</span>
            </button>
          </div>
          <pre className="font-mono text-xs text-gray-300 whitespace-pre-wrap overflow-x-auto leading-relaxed">
            {content || 'Empty markdown.'}
          </pre>
        </div>
      )}
    </div>
  );
};
