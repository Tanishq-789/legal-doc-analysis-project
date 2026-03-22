import { create } from 'zustand';

const useDocStore = create((set) => ({
  docId: null,
  analysisData: null,
  tabValue: 0, // Centralized tab state

  setDocId: (id) => set({ docId: id }),
  setAnalysisData: (data) => set({ analysisData: data }),
  setTabValue: (val) => set({ tabValue: val }),

  resetStore: () => set({ docId: null, analysisData: null, tabValue: 0 })
}));

export default useDocStore;