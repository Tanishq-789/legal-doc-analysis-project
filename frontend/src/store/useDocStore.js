// frontend/src/store/useDocStore.js
import { create } from 'zustand';

const useDocStore = create((set) => ({
  docId: null,
  analysisResults: null, // This stores the JSON from /run
  setDocId: (id) => set({ docId: id }),
  setAnalysisResults: (results) => set({ analysisResults: results }),
}));

export default useDocStore;