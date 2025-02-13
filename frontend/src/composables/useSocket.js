import { getCurrentInstance } from "vue";

export function useSocket() {
  const internalInstance = getCurrentInstance();
  return internalInstance.appContext.config.globalProperties.$socket;
}
