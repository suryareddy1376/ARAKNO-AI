import React, { useState, useEffect } from 'react';
import {
  FileCheck,
  Plus,
  ShieldCheck,
  CheckCircle2,
  XCircle,
  Filter,
  ExternalLink,
  Search,
} from 'lucide-react';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { EmptyState } from '../../components/common/EmptyState';
import { getEvidenceRecords, createEvidenceRecord, verifyCitation } from '../../services/evidence';
import { EvidenceRecord } from '../../types/evidence';
import { useNotificationStore } from '../../stores/notificationStore';

const CATEGORY_MAP: Record<string, { label: string; desc: string; color: string }> = {
  A: { label: 'Human clinical', desc: 'Patient cohorts, clinical trials', color: '#10b981' },
  B: { label: 'Animal experimental', desc: 'In vivo animal models', color: '#f59e0b' },
  C: { label: 'Cell and laboratory', desc: 'In vitro, cell lines, bench assays', color: '#3b82f6' },
  D: { label: 'Computational predictions', desc: 'Finite element, molecular modeling', color: '#8b5cf6' },
  E: { label: 'Theoretical hypotheses', desc: 'Frameworks, expert consensus', color: '#ec4899' },
};

export const EvidencePage: React.FC = () => {
  const { addToast } = useNotificationStore();
  const [evidenceList, setEvidenceList] = useState<EvidenceRecord[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);

  // Filter state
  const [selectedCategory, setSelectedCategory] = useState<string>('all');

  // Form state
  const [newClaim, setNewClaim] = useState('');
  const [newCategory, setNewCategory] = useState('A');
  const [newType, setNewType] = useState('experimental');
  const [newStrength, setNewStrength] = useState('moderate');
  const [newSection, setNewSection] = useState('Results');

  // Citation verify state
  const [verifyPmid, setVerifyPmid] = useState('');
  const [verifyResult, setVerifyResult] = useState<any>(null);
  const [isVerifying, setIsVerifying] = useState(false);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const res = await getEvidenceRecords({
        page_size: 50,
      });
      setEvidenceList(res.items);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreate = async () => {
    if (!newClaim.trim()) return;
    try {
      await createEvidenceRecord({
        claim: newClaim,
        evidence_type: newType,
        strength: newStrength,
        source_section: newSection,
        verified: false,
      });
      addToast({ type: 'success', message: 'Evidence record created' });
      setShowCreateModal(false);
      setNewClaim('');
      loadData();
    } catch (e) {
      addToast({ type: 'error', message: 'Failed to create evidence' });
    }
  };

  const handleVerify = async () => {
    if (!verifyPmid.trim()) return;
    setIsVerifying(true);
    try {
      const res = await verifyCitation({ pmid: verifyPmid });
      setVerifyResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsVerifying(false);
    }
  };

  const filteredEvidence = evidenceList;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Evidence library"
        subtitle="Scientific claims grouped into categories A through E with primary citations."
        badge="Evidence base"
        actions={
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow-sm"
          >
            <Plus className="w-4 h-4" />
            Add claim
          </button>
        }
      />

      {/* Category Definitions Overview */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
        {Object.entries(CATEGORY_MAP).map(([cat, info]) => (
          <div
            key={cat}
            className="rounded-lg border border-[#30363d] bg-[#161b22] p-3 text-xs space-y-1"
          >
            <div className="flex items-center gap-2">
              <span
                className="w-5 h-5 rounded-full flex items-center justify-center font-bold text-[11px] text-white"
                style={{ backgroundColor: info.color }}
              >
                {cat}
              </span>
              <span className="font-medium text-[#e6edf3]">{info.label}</span>
            </div>
            <p className="text-[11px] text-[#8b949e]">{info.desc}</p>
          </div>
        ))}
      </div>

      {/* Citation Verification Tool */}
      <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-3">
        <h3 className="text-xs font-semibold text-[#e6edf3] flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-blue-400" />
          Citation verification
        </h3>
        <div className="flex gap-3">
          <input
            type="text"
            value={verifyPmid}
            onChange={(e) => setVerifyPmid(e.target.value)}
            placeholder="Enter PMID (such as 35272101) or DOI to verify primary source..."
            className="flex-1 bg-[#0f1117] border border-[#30363d] rounded-md px-3 py-2 text-xs text-[#e6edf3] focus:border-blue-500 focus:outline-none"
          />
          <button
            onClick={handleVerify}
            disabled={isVerifying || !verifyPmid.trim()}
            className="px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition"
          >
            {isVerifying ? 'Checking...' : 'Verify citation'}
          </button>
        </div>

        {verifyResult && (
          <div
            className={`p-3 rounded-md text-xs border ${
              verifyResult.valid
                ? 'bg-emerald-950/20 border-emerald-800 text-emerald-200'
                : 'bg-rose-950/20 border-rose-800 text-rose-200'
            }`}
          >
            <div className="flex items-center gap-2 font-medium">
              {verifyResult.valid ? <CheckCircle2 className="w-4 h-4 text-emerald-400" /> : <XCircle className="w-4 h-4 text-rose-400" />}
              <span>{verifyResult.verification_message}</span>
            </div>
            {verifyResult.title && <p className="mt-1 text-[#e6edf3]">{verifyResult.title}</p>}
            {verifyResult.journal && (
              <p className="text-[11px] text-gray-400 mt-0.5">
                {verifyResult.journal} ({verifyResult.year})
              </p>
            )}
          </div>
        )}
      </div>

      {/* Evidence List */}
      {isLoading ? (
        <LoadingState message="Loading evidence records..." />
      ) : filteredEvidence.length === 0 ? (
        <EmptyState
          icon={FileCheck}
          title="No evidence records"
          description="Evidence claims appear here once extracted from papers or added manually."
          actionLabel="Add first claim"
          onAction={() => setShowCreateModal(true)}
        />
      ) : (
        <div className="space-y-3">
          {filteredEvidence.map((ev) => (
            <div
              key={ev.id}
              className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 flex items-start justify-between gap-4"
            >
              <div className="space-y-1.5 flex-1">
                <div className="flex items-center gap-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-medium uppercase tracking-wider bg-blue-950/60 text-blue-300 border border-blue-800/40">
                    {ev.evidence_type}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] font-medium uppercase tracking-wider bg-gray-800 text-gray-300">
                    Strength: {ev.strength}
                  </span>
                  {ev.verified ? (
                    <span className="flex items-center gap-1 text-[11px] text-emerald-400 font-medium">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Verified citation
                    </span>
                  ) : (
                    <span className="text-[11px] text-gray-500">Unverified</span>
                  )}
                </div>
                <p className="text-xs font-medium text-[#e6edf3] leading-relaxed">{ev.claim}</p>
                {ev.source_section && (
                  <span className="text-[10px] text-[#8b949e]">Section: {ev.source_section}</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 max-w-lg w-full space-y-4">
            <h3 className="text-base font-semibold text-[#e6edf3]">Add evidence claim</h3>
            <div>
              <label className="block text-xs font-medium text-[#8b949e] mb-1">Claim statement</label>
              <textarea
                value={newClaim}
                onChange={(e) => setNewClaim(e.target.value)}
                rows={3}
                placeholder="State the biological or biomechanical finding..."
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3] focus:outline-none"
              />
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-[#8b949e] mb-1">Evidence type</label>
                <select
                  value={newType}
                  onChange={(e) => setNewType(e.target.value)}
                  className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
                >
                  <option value="experimental">Experimental assays</option>
                  <option value="citation">Literature citation</option>
                  <option value="computational">Computational simulation</option>
                  <option value="review">Systematic review</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-medium text-[#8b949e] mb-1">Strength</label>
                <select
                  value={newStrength}
                  onChange={(e) => setNewStrength(e.target.value)}
                  className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
                >
                  <option value="strong">Strong</option>
                  <option value="moderate">Moderate</option>
                  <option value="weak">Weak</option>
                  <option value="contradictory">Contradictory</option>
                </select>
              </div>
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-3 py-1.5 rounded text-xs text-gray-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={!newClaim.trim()}
                className="px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white shadow-sm"
              >
                Save claim
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
