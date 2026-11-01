import React, { useState } from 'react';
import {
  Dna,
  FileCode,
  GitCompare,
  Layers,
  Upload,
  Play,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { analyzeFastaText, compareSequences, analyzeStructureFile } from '../../services/biology';
import { FastaAnalysisResponse, SequenceComparisonResponse, StructureAnalysisResponse } from '../../types/biology';

export const BiologyPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'fasta' | 'alignment' | 'structure'>('fasta');

  // FASTA state
  const [fastaInput, setFastaInput] = useState(
    '>sp|P02452|CO1A1_HUMAN Collagen alpha-1(I) chain (N-terminal propeptide)\nMFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPVTCVQNGLRYHDRDVWKPEPCRICVCDNGKVLCDDVI'
  );
  const [fastaResult, setFastaResult] = useState<FastaAnalysisResponse | null>(null);
  const [isAnalyzingFasta, setIsAnalyzingFasta] = useState(false);

  // Alignment state
  const [seq1, setSeq1] = useState('MFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPVT');
  const [seq2, setSeq2] = useState('MFSFVDLRLLLLLAATALLTHGQEEGQVEGQDEDIPPAT');
  const [alignmentMode, setAlignmentMode] = useState<'global' | 'local'>('global');
  const [alignmentResult, setAlignmentResult] = useState<SequenceComparisonResponse | null>(null);
  const [isAligning, setIsAligning] = useState(false);

  // Structure upload state
  const [structureResult, setStructureResult] = useState<StructureAnalysisResponse | null>(null);
  const [isAnalyzingStructure, setIsAnalyzingStructure] = useState(false);

  const handleAnalyzeFasta = async () => {
    if (!fastaInput.trim()) return;
    setIsAnalyzingFasta(true);
    try {
      const res = await analyzeFastaText(fastaInput, 'protein');
      setFastaResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAnalyzingFasta(false);
    }
  };

  const handleCompareSequences = async () => {
    if (!seq1.trim() || !seq2.trim()) return;
    setIsAligning(true);
    try {
      const res = await compareSequences(seq1, seq2, alignmentMode);
      setAlignmentResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsAligning(false);
    }
  };

  const handleStructureFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setIsAnalyzingStructure(true);
    try {
      const format = file.name.endsWith('.cif') ? 'cif' : 'pdb';
      const res = await analyzeStructureFile(file, format);
      setStructureResult(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsAnalyzingStructure(false);
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Computational biology"
        subtitle="Sequence statistics, pairwise alignment, and structure coordinate summaries."
        badge="Biopython"
        actions={
          <div className="flex rounded-md bg-[#161b22] border border-[#30363d] p-1">
            <button
              onClick={() => setActiveTab('fasta')}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                activeTab === 'fasta' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              FASTA analyzer
            </button>
            <button
              onClick={() => setActiveTab('alignment')}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                activeTab === 'alignment' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              Pairwise alignment
            </button>
            <button
              onClick={() => setActiveTab('structure')}
              className={`px-3 py-1 rounded text-xs font-medium transition ${
                activeTab === 'structure' ? 'bg-blue-600 text-white' : 'text-gray-400 hover:text-white'
              }`}
            >
              Structure parser
            </button>
          </div>
        }
      />

      {/* FASTA Analyzer Tab */}
      {activeTab === 'fasta' && (
        <div className="space-y-6">
          <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-4">
            <label className="block text-xs font-medium text-[#8b949e]">
              FASTA header and sequence
            </label>
            <textarea
              value={fastaInput}
              onChange={(e) => setFastaInput(e.target.value)}
              rows={5}
              className="w-full rounded-md bg-[#0f1117] border border-[#30363d] p-3 text-xs font-mono text-[#e6edf3] focus:border-blue-500 focus:outline-none transition"
            />
            <div className="flex justify-end">
              <button
                onClick={handleAnalyzeFasta}
                disabled={isAnalyzingFasta || !fastaInput.trim()}
                className="flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow-sm"
              >
                <Play className="w-4 h-4 fill-current" />
                {isAnalyzingFasta ? 'Processing...' : 'Analyze FASTA'}
              </button>
            </div>
          </div>

          {fastaResult && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-4">
              <div className="flex items-center justify-between border-b border-[#30363d] pb-3">
                <h3 className="text-sm font-semibold text-[#e6edf3]">
                  Parsed sequences ({fastaResult.total_sequences})
                </h3>
              </div>

              {fastaResult.sequences.map((seq) => (
                <div key={seq.id} className="space-y-4">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                    <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                      <span className="text-[10px] text-gray-500 block">Identifier</span>
                      <span className="text-gray-200 font-mono font-medium">{seq.id}</span>
                    </div>
                    <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                      <span className="text-[10px] text-gray-500 block">Sequence length</span>
                      <span className="text-blue-400 font-mono font-medium">{seq.length} aa</span>
                    </div>
                    <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                      <span className="text-[10px] text-gray-500 block">Molecular weight</span>
                      <span className="text-emerald-400 font-mono font-medium">
                        {seq.molecular_weight ? `${seq.molecular_weight} Da` : 'N/A'}
                      </span>
                    </div>
                    <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                      <span className="text-[10px] text-gray-500 block">Isoelectric point (pI)</span>
                      <span className="text-amber-400 font-mono font-medium">{seq.isoelectric_point || 'N/A'}</span>
                    </div>
                  </div>

                  {seq.amino_acid_composition && (
                    <div className="p-4 rounded bg-[#0f1117] border border-[#30363d] space-y-2">
                      <span className="text-xs font-medium text-gray-300">Amino acid composition (%)</span>
                      <div className="grid grid-cols-5 md:grid-cols-10 gap-2 text-center text-xs">
                        {Object.entries(seq.amino_acid_composition).map(([aa, pct]) => (
                          <div key={aa} className="p-1.5 rounded bg-[#161b22] border border-[#30363d]/60">
                            <span className="font-mono font-medium text-blue-400 block">{aa}</span>
                            <span className="text-[11px] text-gray-400">{pct}%</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Alignment Tab */}
      {activeTab === 'alignment' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 space-y-2">
              <label className="block text-xs font-medium text-[#8b949e]">Sequence 1</label>
              <textarea
                value={seq1}
                onChange={(e) => setSeq1(e.target.value)}
                rows={4}
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs font-mono text-[#e6edf3] focus:outline-none"
              />
            </div>
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-4 space-y-2">
              <label className="block text-xs font-medium text-[#8b949e]">Sequence 2</label>
              <textarea
                value={seq2}
                onChange={(e) => setSeq2(e.target.value)}
                rows={4}
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs font-mono text-[#e6edf3] focus:outline-none"
              />
            </div>
          </div>

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3 text-xs">
              <span className="text-gray-400">Alignment mode:</span>
              <label className="flex items-center gap-1 text-gray-200 cursor-pointer">
                <input
                  type="radio"
                  name="alignMode"
                  checked={alignmentMode === 'global'}
                  onChange={() => setAlignmentMode('global')}
                />
                Global (Needleman-Wunsch)
              </label>
              <label className="flex items-center gap-1 text-gray-200 cursor-pointer">
                <input
                  type="radio"
                  name="alignMode"
                  checked={alignmentMode === 'local'}
                  onChange={() => setAlignmentMode('local')}
                />
                Local (Smith-Waterman)
              </label>
            </div>

            <button
              onClick={handleCompareSequences}
              disabled={isAligning || !seq1.trim() || !seq2.trim()}
              className="flex items-center gap-2 px-4 py-2 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow-sm"
            >
              <GitCompare className="w-4 h-4" />
              {isAligning ? 'Aligning...' : 'Run alignment'}
            </button>
          </div>

          {alignmentResult && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-4">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Sequence identity</span>
                  <span className="text-xl font-bold text-emerald-400 font-mono">
                    {alignmentResult.identity_percentage}%
                  </span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Alignment score</span>
                  <span className="text-xl font-bold text-blue-400 font-mono">
                    {alignmentResult.alignment_score}
                  </span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Identical positions</span>
                  <span className="text-xl font-bold text-gray-200 font-mono">
                    {alignmentResult.matches} / {alignmentResult.alignment_length}
                  </span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Gaps</span>
                  <span className="text-xl font-bold text-amber-400 font-mono">{alignmentResult.gaps}</span>
                </div>
              </div>

              <div className="p-4 rounded bg-[#0f1117] border border-[#30363d] overflow-x-auto font-mono text-xs text-gray-300 space-y-1">
                <div>Seq1: {alignmentResult.aligned_seq1}</div>
                <div>Seq2: {alignmentResult.aligned_seq2}</div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Structure Parser Tab */}
      {activeTab === 'structure' && (
        <div className="space-y-6">
          <div className="rounded-lg border border-dashed border-[#30363d] bg-[#161b22] p-8 text-center space-y-3">
            <Upload className="w-8 h-8 text-gray-400 mx-auto" />
            <div>
              <h4 className="text-sm font-semibold text-[#e6edf3]">Upload PDB or mmCIF structure file</h4>
              <p className="text-xs text-[#8b949e]">Parses chains, residues, and coordinate metrics using Biopython.</p>
            </div>
            <input
              type="file"
              accept=".pdb,.cif,.mmcif"
              onChange={handleStructureFileUpload}
              className="text-xs text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:text-xs file:font-semibold file:bg-blue-600 file:text-white hover:file:bg-blue-500 cursor-pointer"
            />
          </div>

          {structureResult && (
            <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-5 space-y-4">
              <h3 className="text-sm font-semibold text-[#e6edf3]">Structural model summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Chains</span>
                  <span className="text-base font-bold text-blue-400">{structureResult.chains.join(', ') || 'A'}</span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Residues</span>
                  <span className="text-base font-bold text-gray-200">{structureResult.total_residues}</span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Coordinate atoms</span>
                  <span className="text-base font-bold text-gray-200">{structureResult.total_atoms}</span>
                </div>
                <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]">
                  <span className="text-[10px] text-gray-500 block">Mean B-factor or pLDDT</span>
                  <span className="text-base font-bold text-emerald-400">
                    {structureResult.mean_b_factor_or_plddt ?? 'N/A'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
