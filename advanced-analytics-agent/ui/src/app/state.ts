export interface State {
  sessions: Array<string> | null
  newSessionName: string | null,
  activeSession: string | null
  sessionInput: string,
  showSessionInput: boolean,
}

export const initialState: State = {
  activeSession: null,
  newSessionName: null,
  sessions: null,
  sessionInput: "",
  showSessionInput: false,
}

export function fixSessionIdFromRawId(rawSessionId: string) {
  return rawSessionId.replaceAll("DataAnalyticsAgent:", "");
}

export function stateReducer(state: State, action: any) {
  switch (action.type) {
    case 'setSessionIds':
      const sessions = action.sessions.map(fixSessionIdFromRawId)
      return { ...state, sessions: sessions, newSessionName: !sessions.includes(state.newSessionName) ? state.newSessionName : null };
    case 'setActiveSessionId':
      const id = fixSessionIdFromRawId(action.id);
      return { ...state, activeSession: id };
    case 'toggleSessionInput':
      return { ...state, showSessionInput: !state.showSessionInput, sessionInput: "" };
    case 'setSessionInput':
      return { ...state, sessionInput: action.value };
    case 'addSession':
      return { ...state, activeSession: action.id, newSessionName: action.id };
    default:
      throw "invalid action " + JSON.stringify(action)
  }
}