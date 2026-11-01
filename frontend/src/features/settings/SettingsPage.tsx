import React, { useState, useEffect } from 'react';
import {
  Settings,
  ShieldCheck,
  Server,
  Lock,
  Database,
  Cpu,
  Mail,
  RefreshCw,
  CheckCircle2,
  AlertTriangle,
} from 'lucide-react';

import { PageHeader } from '../../components/common/PageHeader';
import { LoadingState } from '../../components/common/LoadingState';
import {
  getSystemSettings,
  updateSystemSettings,
  getProviderStatus,
} from '../../services/settings';
import { SystemSettings as ISystemSettings, ProviderStatus } from '../../types/settings';
import { useNotificationStore } from '../../stores/notificationStore';

export const SettingsPage: React.FC = () => {
  const { addToast } = useNotificationStore();
  const [settings, setSettings] = useState<ISystemSettings | null>(null);
  const [providers, setProviders] = useState<ProviderStatus[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);

  // Form states
  const [ncbiEmail, setNcbiEmail] = useState('');
  const [selectedProvider, setSelectedProvider] = useState('none');
  const [llmModel, setLlmModel] = useState('');
  const [llmApiKey, setLlmApiKey] = useState('');
  const [privacyMode, setPrivacyMode] = useState(true);

  const loadData = async () => {
    setIsLoading(true);
    try {
      const [s, p] = await Promise.all([getSystemSettings(), getProviderStatus()]);
      setSettings(s);
      setProviders(p);
      setNcbiEmail(s.ncbi_email_configured ? 'Configured in .env' : '');
      setSelectedProvider(s.llm_provider);
      setLlmModel(s.llm_model);
      setPrivacyMode(s.privacy_mode);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSave = async () => {
    setIsSaving(true);
    try {
      const updates: any = {
        llm_provider: selectedProvider,
        llm_model: llmModel,
        privacy_mode: privacyMode,
      };
      if (ncbiEmail && ncbiEmail !== 'Configured in .env') {
        updates.ncbi_email = ncbiEmail;
      }
      if (llmApiKey) {
        updates.llm_api_key = llmApiKey;
      }

      const updated = await updateSystemSettings(updates);
      setSettings(updated);
      setLlmApiKey(''); // Never keep API key in form state
      addToast({ type: 'success', message: 'Settings updated successfully' });
      const provs = await getProviderStatus();
      setProviders(provs);
    } catch (e) {
      addToast({ type: 'error', message: 'Failed to update settings' });
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) return <LoadingState message="Loading system configuration..." />;

  return (
    <div className="space-y-6">
      <PageHeader
        title="Settings"
        subtitle="Configure local storage directories, NCBI contact email, and optional model providers."
        badge="System settings"
      />

      {/* Privacy and Cost Enforcement Notice */}
      <div className="rounded-lg border border-emerald-900/40 bg-emerald-950/10 p-5 flex items-start gap-3 text-xs text-emerald-200">
        <ShieldCheck className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="font-semibold text-sm text-emerald-300">Local execution and privacy defaults</h4>
          <p className="text-gray-300 leading-relaxed">
            The application runs with <code>LLM_PROVIDER=none</code> by default.
            Paid endpoints and automatic model switching are disabled. Sensitive files remain in local
            storage and are never sent to remote services.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Card: AI Provider Selection */}
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-5">
          <h3 className="text-sm font-semibold text-[#e6edf3] flex items-center gap-2">
            <Cpu className="w-4 h-4 text-blue-400" />
            Model provider
          </h3>

          <div>
            <label className="block text-xs font-medium text-[#8b949e] mb-1.5">Provider</label>
            <select
              value={selectedProvider}
              onChange={(e) => setSelectedProvider(e.target.value)}
              className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs text-[#e6edf3] focus:outline-none"
            >
              <option value="none">None (deterministic local extraction, default)</option>
              <option value="nvidia">NVIDIA Nemotron (integrate.api.nvidia.com)</option>
              <option value="ollama">Ollama (local daemon at localhost:11434)</option>
              <option value="openrouter">OpenRouter (free models only)</option>
              <option value="gemini">Google Gemini API</option>
            </select>
          </div>

          {selectedProvider !== 'none' && (
            <>
              <div>
                <label className="block text-xs font-medium text-[#8b949e] mb-1.5">Model identifier</label>
                <input
                  type="text"
                  value={llmModel}
                  onChange={(e) => setLlmModel(e.target.value)}
                  placeholder="such as llama3.2:latest or meta-llama/llama-3.2-3b-instruct:free"
                  className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs text-[#e6edf3] focus:outline-none"
                />
              </div>

              {selectedProvider !== 'ollama' && (
                <div>
                  <label className="block text-xs font-medium text-[#8b949e] mb-1.5">
                    API key (stored in local environment, never displayed)
                  </label>
                  <input
                    type="password"
                    value={llmApiKey}
                    onChange={(e) => setLlmApiKey(e.target.value)}
                    placeholder="Enter API key to update..."
                    className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs text-[#e6edf3] focus:outline-none"
                  />
                </div>
              )}
            </>
          )}

          {/* Provider Status Diagnostic List */}
          <div className="space-y-2 pt-3 border-t border-[#30363d]/50">
            <span className="text-[11px] font-medium text-gray-400 block uppercase tracking-wider">
              Provider status
            </span>
            {providers.map((p) => (
              <div
                key={p.provider}
                className="flex items-center justify-between p-2.5 rounded bg-[#0f1117] border border-[#30363d]/40 text-xs"
              >
                <div className="flex items-center gap-2">
                  <span
                    className={`w-2 h-2 rounded-full ${
                      p.is_available ? 'bg-emerald-500' : 'bg-gray-600'
                    }`}
                  />
                  <span className="font-medium text-gray-200 capitalize">{p.provider}</span>
                </div>
                <span className="text-[11px] text-gray-400">{p.message}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Right Card: Storage & External APIs */}
        <div className="rounded-lg border border-[#30363d] bg-[#161b22] p-6 space-y-5">
          <h3 className="text-sm font-semibold text-[#e6edf3] flex items-center gap-2">
            <Server className="w-4 h-4 text-cyan-400" />
            Storage and data sources
          </h3>

          <div>
            <label className="block text-xs font-medium text-[#8b949e] mb-1.5">
              NCBI contact email
            </label>
            <input
              type="email"
              value={ncbiEmail}
              onChange={(e) => setNcbiEmail(e.target.value)}
              placeholder="researcher@institution.edu"
              className="w-full rounded bg-[#0f1117] border border-[#30363d] p-2.5 text-xs text-[#e6edf3] focus:outline-none"
            />
            <span className="text-[10px] text-gray-400 mt-1 block">
              NCBI requests an email for E-utilities queries to prevent throttling.
            </span>
          </div>

          <div className="space-y-2.5 pt-2">
            <span className="text-xs font-medium text-gray-300 block">Local file paths:</span>
            <div className="p-3 rounded bg-[#0f1117] border border-[#30363d]/60 font-mono text-[11px] text-gray-300 space-y-1">
              <div>Database: <code>./data/database/arakno.db</code></div>
              <div>Structures: <code>{settings?.structures_dir}</code></div>
              <div>Reports: <code>{settings?.reports_dir}</code></div>
              <div>Private case: <code>./data/private_case/ (isolated)</code></div>
            </div>
          </div>

          <div className="pt-4 border-t border-[#30363d]/50 flex justify-end">
            <button
              onClick={handleSave}
              disabled={isSaving}
              className="px-5 py-2 rounded-md bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white text-xs font-medium transition shadow-sm"
            >
              {isSaving ? 'Saving changes...' : 'Save changes'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
