import React, { useState, useEffect } from 'react';
import {
  Building2,
  FolderKanban,
  HelpCircle,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { getResearchDivisions, getProjects } from '../../services/projects';
import { ResearchDivision, ResearchProject } from '../../types/research';

export const DivisionsPage: React.FC = () => {
  const [divisions, setDivisions] = useState<ResearchDivision[]>([]);
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [selectedDivision, setSelectedDivision] = useState<ResearchDivision | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [divs, projs] = await Promise.all([
          getResearchDivisions(),
          getProjects(),
        ]);
        setDivisions(divs);
        setProjects(projs);
        if (divs.length > 0) {
          setSelectedDivision(divs[0]);
        }
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    };
    fetchData();
  }, []);

  if (isLoading) return <LoadingState message="Loading research divisions..." />;

  const divisionProjects = projects.filter(
    (p) => p.division_id === selectedDivision?.id
  );

  return (
    <div className="space-y-6">
      <PageHeader
        title="Research divisions"
        subtitle="Research programmes covering spinal biomechanics, bone regeneration, biomaterials, and sensory biology."
        badge="6 divisions"
      />

      {/* Grid of 6 Divisions */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {divisions.map((div) => {
          const isSelected = selectedDivision?.id === div.id;
          const count = projects.filter((p) => p.division_id === div.id).length;

          return (
            <div
              key={div.id}
              onClick={() => setSelectedDivision(div)}
              className={`rounded-lg border p-5 cursor-pointer transition flex flex-col justify-between ${
                isSelected
                  ? 'border-blue-500 bg-[#1c2333] shadow-md ring-1 ring-blue-500/50'
                  : 'border-[#30363d] bg-[#161b22] hover:border-gray-600 hover:bg-[#1a202c]'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: div.color }}
                    />
                    <h3 className="text-sm font-semibold text-[#e6edf3]">{div.name}</h3>
                  </div>
                  <span className="text-[11px] font-mono text-gray-400">
                    {count} {count === 1 ? 'project' : 'projects'}
                  </span>
                </div>
                <p className="text-xs text-[#8b949e] leading-relaxed line-clamp-3">
                  {div.description}
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-[#30363d]/50 flex items-center justify-between text-xs font-medium text-blue-400">
                <span>View division projects</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Selected Division Workspace */}
      {selectedDivision && (
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-6">
          <div className="border-b border-[#30363d] pb-4">
            <div className="flex items-center gap-3">
              <span
                className="w-4 h-4 rounded-full"
                style={{ backgroundColor: selectedDivision.color }}
              />
              <h2 className="text-lg font-semibold text-[#e6edf3]">
                {selectedDivision.name}
              </h2>
            </div>
            <p className="text-xs text-[#8b949e] mt-2 leading-relaxed">
              {selectedDivision.description}
            </p>
          </div>

          <div className="space-y-4">
            <h3 className="text-xs font-semibold text-[#e6edf3] flex items-center gap-2">
              <FolderKanban className="w-4 h-4 text-blue-400" />
              Projects in this division
            </h3>

            {divisionProjects.length === 0 ? (
              <p className="text-xs text-gray-500">
                No projects assigned to this division. Create one from the research projects view.
              </p>
            ) : (
              <div className="space-y-4">
                {divisionProjects.map((p) => (
                  <div
                    key={p.id}
                    className="rounded-lg border border-[#30363d] bg-[#0f1117] p-4 space-y-3"
                  >
                    <div className="flex items-start justify-between">
                      <div>
                        <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-blue-950/60 text-blue-300 border border-blue-800/40">
                          {p.id}
                        </span>
                        <h4 className="text-sm font-semibold text-[#e6edf3] mt-1.5">{p.title}</h4>
                        <p className="text-xs text-[#8b949e] mt-1">{p.description}</p>
                      </div>
                      <span className="text-[11px] font-medium text-emerald-400 uppercase tracking-wider px-2 py-0.5 rounded bg-emerald-950/40 border border-emerald-800/40">
                        {p.status}
                      </span>
                    </div>

                    {p.questions && p.questions.length > 0 && (
                      <div className="pt-2 border-t border-[#30363d]/40 space-y-1.5">
                        <span className="text-[11px] font-medium text-gray-400 block">
                          Research questions:
                        </span>
                        {p.questions.map((q) => (
                          <div
                            key={q.id}
                            className="flex items-start gap-2 text-xs text-gray-300"
                          >
                            <HelpCircle className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                            <span>{q.question}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
