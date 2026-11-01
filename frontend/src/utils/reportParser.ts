/**
 * Utilities to parse ARAKNO-AI Markdown research reports into structured objects.
 */

export interface ParsedTarget {
  symbol: string;
  name: string;
  accession: string;
  organism: string;
  plddt?: string;
}

export interface ParsedEvidence {
  sourceTitle: string;
  sourceUrl?: string;
  pmid?: string;
  doi?: string;
  year?: string;
  journal?: string;
  category: string;
  strength: string;
  finding: string;
}

export interface ParsedReference {
  index: number;
  title: string;
  authors?: string;
  journal?: string;
  year?: string;
  pmid?: string;
  doi?: string;
}

export interface ParsedReportData {
  title: string;
  executiveSummary: string;
  targets: ParsedTarget[];
  evidence: ParsedEvidence[];
  verificationStatus: string;
  verificationSummary: string;
  references: ParsedReference[];
  aiSynthesis?: string;
  publicationCount: number;
  evidenceCount: number;
  targetsCount: number;
}

export function parseMarkdownReport(content: string, fallbackTitle: string = 'Research Report'): ParsedReportData {
  const result: ParsedReportData = {
    title: fallbackTitle,
    executiveSummary: '',
    targets: [],
    evidence: [],
    verificationStatus: 'VERIFIED',
    verificationSummary: 'All citations verified against primary databases.',
    references: [],
    publicationCount: 0,
    evidenceCount: 0,
    targetsCount: 0,
  };

  if (!content || !content.trim()) return result;

  // Extract title if present (# Research Report: ...)
  const titleMatch = content.match(/^#\s+(?:Research Report:\s*)?([^\n]+)/m);
  if (titleMatch) {
    result.title = titleMatch[1].trim();
  }

  // Section splitting
  const sections = content.split(/^##\s+/m);

  for (const sec of sections) {
    const trimmed = sec.trim();
    if (!trimmed) continue;

    const firstLineEnd = trimmed.indexOf('\n');
    const header = firstLineEnd !== -1 ? trimmed.slice(0, firstLineEnd).trim().toLowerCase() : trimmed.toLowerCase();
    const body = firstLineEnd !== -1 ? trimmed.slice(firstLineEnd).trim() : '';

    // 1. Executive Summary
    if (header.includes('executive summary') || header.startsWith('1.')) {
      result.executiveSummary = body.replace(/^>+[^\n]*\n?/gm, '').trim();

      // Try extract counts from summary (e.g. total of **25** peer-reviewed publications... Identified 23 verifiable...)
      const pubMatch = body.match(/(\d+)\s+peer-reviewed publications/i);
      if (pubMatch) result.publicationCount = parseInt(pubMatch[1], 10);

      const evMatch = body.match(/Identified\s+(\d+)\s+verifiable/i);
      if (evMatch) result.evidenceCount = parseInt(evMatch[1], 10);

      const tgMatch = body.match(/(\d+)\s+structural macromolecular targets/i);
      if (tgMatch) result.targetsCount = parseInt(tgMatch[1], 10);
    }

    // 2. Biological Targets
    else if (header.includes('biological targets') || header.startsWith('2.')) {
      const lines = body.split('\n');
      let currentTarget: ParsedTarget | null = null;

      for (const line of lines) {
        const l = line.trim();
        // Target line: - **COL1A1** (Collagen alpha-1(I) chain) — UniProt: `P02452`, Organism: *Homo sapiens*
        const targetMatch = l.match(/^-\s+\*\*([^*]+)\*\*\s*\(([^)]+)\)[^`]*`([^`]+)`[^*]*\*([^*]+)\*/i);
        if (targetMatch) {
          currentTarget = {
            symbol: targetMatch[1].trim(),
            name: targetMatch[2].trim(),
            accession: targetMatch[3].trim(),
            organism: targetMatch[4].trim(),
          };
          result.targets.push(currentTarget);
        } else if (currentTarget && l.includes('AlphaFold Global pLDDT:')) {
          const plddtMatch = l.match(/\*\*([0-9.]+)\*\*/);
          if (plddtMatch) {
            currentTarget.plddt = plddtMatch[1];
          }
        }
      }
    }

    // 3. Evidence Matrix
    else if (header.includes('evidence matrix') || header.startsWith('3.')) {
      const rows = body.split('\n').filter((r) => r.trim().startsWith('|'));
      // Skip header and separator row
      const dataRows = rows.slice(2);

      for (const row of dataRows) {
        const cols = row.split('|').map((c) => c.trim()).filter((_, idx, arr) => idx > 0 && idx < arr.length - 1);
        if (cols.length >= 6) {
          const sourceRaw = cols[0];
          let sourceTitle = sourceRaw;
          let sourceUrl: string | undefined = undefined;
          let pmid: string | undefined = undefined;

          const linkMatch = sourceRaw.match(/\[([^\]]+)\]\(([^)]+)\)/);
          if (linkMatch) {
            sourceTitle = linkMatch[1];
            sourceUrl = linkMatch[2];
            const pmidMatch = sourceUrl.match(/pubmed\.ncbi\.nlm\.nih\.gov\/(\d+)/);
            if (pmidMatch) pmid = pmidMatch[1];
          }

          result.evidence.push({
            sourceTitle,
            sourceUrl,
            pmid,
            year: cols[1] !== 'N/A' ? cols[1] : undefined,
            journal: cols[2] !== 'N/A' ? cols[2] : undefined,
            category: cols[3].replace(/^Cat\s*/i, '').trim(),
            strength: cols[4].trim(),
            finding: cols[5].replace(/\.\.\.$/, '').trim(),
          });
        }
      }
    }

    // 4. Citation Verification
    else if (header.includes('citation') || header.includes('traceability') || header.startsWith('4.')) {
      const statusMatch = body.match(/Status:\s*\*\*([^*]+)\*\*/i);
      if (statusMatch) result.verificationStatus = statusMatch[1].trim();

      const summaryMatch = body.match(/Traceability:\s*([^\n]+)/i);
      if (summaryMatch) result.verificationSummary = summaryMatch[1].trim();
    }

    // 5. References
    else if (header.includes('references') || header.startsWith('5.')) {
      const lines = body.split('\n');
      for (const line of lines) {
        const l = line.trim();
        const refMatch = l.match(/^(\d+)\.\s+\*\*([^*]+)\*\*\.(?:[^*]*\*([^*]+)\*,)?(?:\s*(\d{4}))?/i);
        if (refMatch) {
          const idx = parseInt(refMatch[1], 10);
          const title = refMatch[2].trim();
          const journal = refMatch[3]?.trim();
          const year = refMatch[4]?.trim();

          const pmidMatch = l.match(/PMID:\s*\[?(\d+)\]?/i);
          const doiMatch = l.match(/DOI:\s*\[?([10\.\d+\/[^\s\]]+)\]?/i);

          result.references.push({
            index: idx,
            title,
            journal,
            year,
            pmid: pmidMatch ? pmidMatch[1] : undefined,
            doi: doiMatch ? doiMatch[1] : undefined,
          });
        }
      }
    }

    // 6. AI Evidence Synthesis
    else if (header.includes('ai evidence synthesis') || header.includes('ai synthesis') || header.startsWith('6.')) {
      result.aiSynthesis = body.trim();
    }
  }

  // Fallback counters if not explicitly mentioned in summary
  if (!result.publicationCount && result.references.length > 0) {
    result.publicationCount = result.references.length;
  }
  if (!result.evidenceCount && result.evidence.length > 0) {
    result.evidenceCount = result.evidence.length;
  }
  if (!result.targetsCount && result.targets.length > 0) {
    result.targetsCount = result.targets.length;
  }

  return result;
}
