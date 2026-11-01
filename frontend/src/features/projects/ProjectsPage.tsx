import React, { useState, useEffect } from 'react';
import {
  FolderKanban,
  Plus,
  HelpCircle,
  Clock,
  CheckCircle2,
  Tag,
  Building2,
} from 'lucide-react';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import { EmptyState } from '../../components/common/EmptyState';
import { getProjects, createProject, addProjectQuestion, getResearchDivisions } from '../../services/projects';
import { ResearchProject, ResearchDivision } from '../../types/research';
import { useNotificationStore } from '../../stores/notificationStore';

export const ProjectsPage: React.FC = () => {
  const { addToast } = useNotificationStore();
  const [projects, setProjects] = useState<ResearchProject[]>([]);
  const [divisions, setDivisions] = useState<ResearchDivision[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  // Modals state
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showQuestionModal, setShowQuestionModal] = useState<string | null>(null);

  // Form states
  const [projCode, setProjCode] = useState('');
  const [projTitle, setProjTitle] = useState('');
  const [projDesc, setProjDesc] = useState('');
  const [selectedDivId, setSelectedDivId] = useState<number | undefined>(undefined);

  const [questionText, setQuestionText] = useState('');

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [projs, divs] = await Promise.all([getProjects(), getResearchDivisions()]);
      setProjects(projs);
      setDivisions(divs);
      if (divs.length > 0) setSelectedDivId(divs[0].id);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateProject = async () => {
    if (!projTitle.trim()) return;
    try {
      await createProject({
        id: projCode.trim() || undefined,
        title: projTitle,
        description: projDesc,
        division_id: selectedDivId,
        status: 'active',
      });
      addToast({ type: 'success', message: 'Project created successfully' });
      setShowCreateModal(false);
      setProjCode('');
      setProjTitle('');
      setProjDesc('');
      loadData();
    } catch (e) {
      addToast({ type: 'error', message: 'Failed to create project' });
    }
  };

  const handleAddQuestion = async (projectId: string) => {
    if (!questionText.trim()) return;
    try {
      await addProjectQuestion(projectId, { question: questionText });
      addToast({ type: 'success', message: 'Research question added' });
      setShowQuestionModal(null);
      setQuestionText('');
      loadData();
    } catch (e) {
      addToast({ type: 'error', message: 'Failed to add question' });
    }
  };

  return (
    <div className="space-y-6">
      <PageHeader
        title="Research projects"
        subtitle="Manage research programmes, hypotheses, and open questions."
        badge="Projects"
        actions={
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-md bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium transition shadow-sm"
          >
            <Plus className="w-4 h-4" />
            New project
          </button>
        }
      />

      {isLoading ? (
        <LoadingState message="Loading projects..." />
      ) : projects.length === 0 ? (
        <EmptyState
          icon={FolderKanban}
          title="No research projects"
          description="Create a project to organize papers, proteins, and evidence."
          actionLabel="Create project"
          onAction={() => setShowCreateModal(true)}
        />
      ) : (
        <div className="space-y-6">
          {projects.map((proj) => (
            <div
              key={proj.id}
              className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-4 shadow-sm"
            >
              <div className="flex flex-col md:flex-row md:items-start justify-between gap-4 border-b border-[#30363d]/50 pb-4">
                <div>
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="font-mono text-xs font-medium px-2.5 py-0.5 rounded bg-blue-950/70 text-blue-300 border border-blue-800/40">
                      {proj.id}
                    </span>
                    {proj.division && (
                      <span
                        className="text-xs font-medium px-2 py-0.5 rounded border"
                        style={{
                          backgroundColor: `${proj.division.color}18`,
                          borderColor: `${proj.division.color}40`,
                          color: proj.division.color,
                        }}
                      >
                        {proj.division.name}
                      </span>
                    )}
                    <span className="text-xs font-medium text-emerald-400 uppercase tracking-wider">
                      {proj.status}
                    </span>
                  </div>
                  <h3 className="text-base font-semibold text-[#e6edf3] mt-2">{proj.title}</h3>
                  {proj.description && (
                    <p className="text-xs text-[#8b949e] mt-1.5 leading-relaxed">{proj.description}</p>
                  )}
                </div>

                <button
                  onClick={() => setShowQuestionModal(proj.id)}
                  className="flex items-center gap-1.5 px-3 py-1.5 rounded bg-[#0f1117] border border-[#30363d] hover:border-gray-500 text-xs font-medium text-gray-200 transition shrink-0"
                >
                  <Plus className="w-3.5 h-3.5" />
                  Add question
                </button>
              </div>

              {/* Research Questions List */}
              <div className="space-y-2">
                <span className="text-xs font-medium text-gray-300 uppercase tracking-wider block">
                  Research questions ({proj.questions?.length || 0})
                </span>
                {proj.questions?.length === 0 ? (
                  <p className="text-xs text-gray-500">No questions defined for this project yet.</p>
                ) : (
                  <div className="space-y-2">
                    {proj.questions.map((q) => (
                      <div
                        key={q.id}
                        className="flex items-start gap-2.5 p-3 rounded-md bg-[#0f1117] border border-[#30363d]/40 text-xs text-gray-200"
                      >
                        <HelpCircle className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
                        <div className="flex-1">
                          <p className="font-medium text-[#e6edf3]">{q.question}</p>
                          {q.hypothesis && (
                            <p className="text-[11px] text-[#8b949e] mt-0.5">
                              <em>Hypothesis:</em> {q.hypothesis}
                            </p>
                          )}
                        </div>
                        <span className="text-[10px] font-mono uppercase px-1.5 py-0.5 rounded bg-gray-800 text-gray-400">
                          {q.status}
                        </span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Create Project Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 max-w-lg w-full space-y-4">
            <h3 className="text-base font-semibold text-[#e6edf3]">Create research project</h3>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-[#8b949e] mb-1">Project code</label>
                <input
                  type="text"
                  value={projCode}
                  onChange={(e) => setProjCode(e.target.value)}
                  placeholder="such as ARAKNO-BONE-002"
                  className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-[#8b949e] mb-1">Division</label>
                <select
                  value={selectedDivId}
                  onChange={(e) => setSelectedDivId(Number(e.target.value))}
                  className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
                >
                  {divisions.map((d) => (
                    <option key={d.id} value={d.id}>
                      {d.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-medium text-[#8b949e] mb-1">Project title</label>
              <input
                type="text"
                value={projTitle}
                onChange={(e) => setProjTitle(e.target.value)}
                placeholder="Project title..."
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-[#8b949e] mb-1">Description</label>
              <textarea
                value={projDesc}
                onChange={(e) => setProjDesc(e.target.value)}
                rows={3}
                placeholder="Scope, background, and objectives..."
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setShowCreateModal(false)}
                className="px-3 py-1.5 rounded text-xs text-gray-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateProject}
                disabled={!projTitle.trim()}
                className="px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white shadow-sm"
              >
                Create project
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Add Question Modal */}
      {showQuestionModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
          <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 max-w-md w-full space-y-4">
            <h3 className="text-base font-semibold text-[#e6edf3]">Add research question</h3>
            <div>
              <label className="block text-xs font-medium text-[#8b949e] mb-1">Question</label>
              <textarea
                value={questionText}
                onChange={(e) => setQuestionText(e.target.value)}
                rows={3}
                placeholder="State the biological or mechanical question..."
                className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2 text-xs text-[#e6edf3]"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3">
              <button
                onClick={() => setShowQuestionModal(null)}
                className="px-3 py-1.5 rounded text-xs text-gray-400 hover:text-white"
              >
                Cancel
              </button>
              <button
                onClick={() => handleAddQuestion(showQuestionModal)}
                disabled={!questionText.trim()}
                className="px-4 py-1.5 rounded bg-blue-600 hover:bg-blue-500 text-xs font-medium text-white shadow-sm"
              >
                Add question
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
