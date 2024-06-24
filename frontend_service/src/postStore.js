import { create } from "zustand";

const postStore = (set, get) => ({
  post: '',
  setPost: (post) => {
    set((state) => ({
      post: post,
    }));
  },
  reset: () => {
    set({
      post: '',
    });
  },
});

const usePostStore = create(postStore);

export default usePostStore;