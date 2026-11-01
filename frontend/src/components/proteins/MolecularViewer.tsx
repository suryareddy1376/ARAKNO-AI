import React, { useEffect, useRef, useState } from 'react';
import { RotateCw, ZoomIn, ZoomOut, Maximize2, RefreshCw } from 'lucide-react';

interface MolecularViewerProps {
  accession: string;
  pdbData?: string;
  className?: string;
}

declare global {
  interface Window {
    $3Dmol: any;
  }
}

export const MolecularViewer: React.FC<MolecularViewerProps> = ({
  accession,
  pdbData,
  className = '',
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const viewerRef = useRef<any>(null);
  const [styleMode, setStyleMode] = useState<'cartoon' | 'stick' | 'sphere'>('cartoon');
  const [colorMode, setColorMode] = useState<'plddt' | 'chain' | 'spectrum'>('plddt');
  const [isLoading, setIsLoading] = useState(true);

  // Load 3Dmol.js dynamically if not already present
  useEffect(() => {
    if (!window.$3Dmol) {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js';
      script.async = true;
      script.onload = () => initViewer();
      document.head.appendChild(script);
    } else {
      initViewer();
    }
  }, [pdbData]);

  const initViewer = () => {
    if (!containerRef.current || !window.$3Dmol) return;
    setIsLoading(true);

    try {
      containerRef.current.innerHTML = '';
      const viewer = window.$3Dmol.createViewer(containerRef.current, {
        backgroundColor: '#0f1117',
      });
      viewerRef.current = viewer;

      if (pdbData && pdbData.trim()) {
        viewer.addModel(pdbData, 'pdb');
        applyStyles(viewer, styleMode, colorMode);
        viewer.zoomTo();
        viewer.render();
      }
    } catch (e) {
      console.error('Error rendering 3D molecular structure:', e);
    } finally {
      setIsLoading(false);
    }
  };

  const applyStyles = (viewer: any, style: string, color: string) => {
    if (!viewer) return;

    let colorSpec: any = {};
    if (color === 'plddt') {
      // Color by B-factor / AlphaFold pLDDT
      // >90 blue, 70-90 cyan, 50-70 yellow, <50 orange
      colorSpec = {
        prop: 'b',
        gradient: 'rwb',
        min: 50,
        max: 95,
      };
    } else if (color === 'spectrum') {
      colorSpec = { color: 'spectrum' };
    }

    if (style === 'cartoon') {
      viewer.setStyle({}, { cartoon: { ...colorSpec } });
    } else if (style === 'stick') {
      viewer.setStyle({}, { stick: { ...colorSpec, radius: 0.2 } });
    } else if (style === 'sphere') {
      viewer.setStyle({}, { sphere: { ...colorSpec, scale: 0.3 } });
    }
    viewer.render();
  };

  const handleStyleChange = (newStyle: 'cartoon' | 'stick' | 'sphere') => {
    setStyleMode(newStyle);
    if (viewerRef.current) {
      applyStyles(viewerRef.current, newStyle, colorMode);
    }
  };

  const handleColorChange = (newColor: 'plddt' | 'chain' | 'spectrum') => {
    setColorMode(newColor);
    if (viewerRef.current) {
      applyStyles(viewerRef.current, styleMode, newColor);
    }
  };

  const resetCamera = () => {
    if (viewerRef.current) {
      viewerRef.current.zoomTo();
      viewerRef.current.render();
    }
  };

  return (
    <div className={`flex flex-col rounded-lg border border-[#30363d] bg-[#161b22] overflow-hidden ${className}`}>
      {/* Top Toolbar */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-[#30363d] bg-[#0f1117]/80 text-xs text-[#8b949e]">
        <div className="flex items-center gap-2">
          <span className="font-medium text-[#e6edf3]">3D model: {accession}</span>
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-blue-900/30 text-blue-300 border border-blue-800/40">
            AlphaFold DB
          </span>
        </div>

        <div className="flex items-center gap-2">
          {/* Representation Selector */}
          <select
            value={styleMode}
            onChange={(e) => handleStyleChange(e.target.value as any)}
            className="bg-[#161b22] border border-[#30363d] rounded px-2 py-1 text-xs text-[#e6edf3] focus:outline-none"
          >
            <option value="cartoon">Cartoon ribbon</option>
            <option value="stick">Stick wireframe</option>
            <option value="sphere">Space-filling spheres</option>
          </select>

          {/* Color Scheme Selector */}
          <select
            value={colorMode}
            onChange={(e) => handleColorChange(e.target.value as any)}
            className="bg-[#161b22] border border-[#30363d] rounded px-2 py-1 text-xs text-[#e6edf3] focus:outline-none"
          >
            <option value="plddt">pLDDT score</option>
            <option value="spectrum">Residue spectrum</option>
            <option value="chain">Chain color</option>
          </select>

          {/* Camera Reset */}
          <button
            onClick={resetCamera}
            className="p-1 rounded hover:bg-gray-800 text-gray-300 hover:text-white transition"
            title="Reset view"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* 3D Viewer Canvas Container */}
      <div className="relative w-full h-[460px] bg-[#0f1117]">
        {isLoading && (
          <div className="absolute inset-0 flex items-center justify-center bg-[#0f1117]/80 z-10 text-xs text-blue-400">
            Loading 3Dmol WebGL viewer...
          </div>
        )}
        <div ref={containerRef} className="w-full h-full" />

        {/* pLDDT Legend */}
        {colorMode === 'plddt' && (
          <div className="absolute bottom-3 left-3 bg-[#161b22]/90 backdrop-blur-sm border border-[#30363d] rounded p-2 text-[10px] text-[#e6edf3] space-y-1 z-10">
            <span className="font-medium block mb-1">AlphaFold confidence (pLDDT)</span>
            <div className="flex items-center gap-2">
              <span className="w-3 h-2 rounded-sm bg-[#0053D6]" />
              <span>Very high (pLDDT &gt; 90)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-2 rounded-sm bg-[#65CBF3]" />
              <span>Confident (70 to 90)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-2 rounded-sm bg-[#FFDB13]" />
              <span>Low (50 to 70)</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="w-3 h-2 rounded-sm bg-[#FF7D45]" />
              <span>Very low (below 50)</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
