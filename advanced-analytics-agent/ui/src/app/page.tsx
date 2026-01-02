'use client'
import {
  CopilotKit,
  useCopilotContext,
} from "@copilotkit/react-core";
import { CopilotKitCSSProperties, CopilotChat } from "@copilotkit/react-ui";
import React, { ReactNode, RefObject, useEffect, useReducer, useRef } from "react";
import { fixSessionIdFromRawId, initialState, State, stateReducer } from "./state";
import { useInterval } from "@/lib/hooks";

function PlusIcon({width, height}: {width: number, height: number}) {
  //Font Awesome Free v7.1.0 by @fontawesome - https://fontawesome.com License - https://fontawesome.com/license/free Copyright 2025 Fonticons, Inc.
  return <svg width={width} height={height} xmlns="http://www.w3.org/2000/svg" viewBox="0 0 448 512"><path fill="currentColor" d="M256 64c0-17.7-14.3-32-32-32s-32 14.3-32 32l0 160-160 0c-17.7 0-32 14.3-32 32s14.3 32 32 32l160 0 0 160c0 17.7 14.3 32 32 32s32-14.3 32-32l0-160 160 0c17.7 0 32-14.3 32-32s-14.3-32-32-32l-160 0 0-160z"/></svg>
}

function Main({children}: {children: ReactNode}) {
  return (
    <main
      className="w-screen h-screen"
      style={{ "--copilot-kit-primary-color": "#9c8060ff", "--copilot-kit-background-color": "none"} as CopilotKitCSSProperties}
    >
      {children}
    </main>
  );
}

function pollSessions(state: State, dispatch: ((action: any) => void), setThreadId: ((id: string) => void)) {
    fetch(`/api/sessions`)
      .then(response => response.json())
      .then(json => {
        const sessions = json.sessions;
        dispatch({ type: "setSessionIds", sessions: sessions });
        if (state.activeSession == null && sessions.length > 0) {
          const session = fixSessionIdFromRawId(sessions[sessions.length - 1]);
          dispatch({ type: "setActiveSessionId", id: session });
          setThreadId(session);
        }
      })
}

function PageContent() {
  const { setThreadId } = useCopilotContext(); // TODO 2025-12-17 Move this state out of reducer, this is a hack for the thread ID not updating as regular state
  const [state, dispatch] = useReducer(stateReducer, initialState);

  useInterval(() => {
    pollSessions(state, dispatch, setThreadId);
  }, 2000);

  const switchSessionId = (id: string) => {
    dispatch({type: "setActiveSessionId", id: id})
    setThreadId(id);
  };

  const sessionInputRef: RefObject<HTMLInputElement | null> = useRef(null);
  const toggleSessionInput = () => {
    dispatch({type: "toggleSessionInput"});
  }
  useEffect(() => {
    if (state.showSessionInput) {
      sessionInputRef?.current?.focus();
    }
  }, [state.showSessionInput])
  const updateSessionInput = (event: React.ChangeEvent<HTMLInputElement>) => {
    dispatch({type: "setSessionInput", value: event.target.value})
  }
  const submitSessionOnEnter = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      addSession();
    }
  }
  const addSession = () => {
    if (state.sessionInput == "") {
      return;
    }
    dispatch({type: "addSession", "id": state.sessionInput})
    dispatch({type: "setSessionInput", value: ""})
    dispatch({type: "toggleSessionInput"})
    setThreadId(state.sessionInput);
  }

  const SessionText = ({id, unsubmitted = false}: {id: string, unsubmitted: boolean}) => {
    var classes = id == state.activeSession ? "underline cursor-pointer text-ellipsis" : "cursor-pointer text-ellipsis";
    if (unsubmitted) {
      classes += " italic";
    }
    return (
      <p className={classes}
          key={id} 
          onClick={() => switchSessionId(id)}>
          {id}
      </p>
    );
  };

  return (
    <Main>
      <div className="md:flex">
        <div className="md:min-w-[300px] md:max-w-[224px] text-nowrap p-5 bg-white z-1">
          <div className="flex text-[#9c8060ff] items-center">
            <h2 className="flex-[1] text-md font-bold mb-1">Sessions</h2>
            <span className="cursor-pointer" onClick={() => toggleSessionInput()}>
              <PlusIcon width={16} height={16}/>
            </span>
          </div>
          {state.showSessionInput ? (
            <span className="flex mt-1 mb-2">
              <input placeholder="session name" value={state.sessionInput} ref={sessionInputRef} onKeyDown={submitSessionOnEnter} onChange={updateSessionInput} className="border-b-1 focus:outline-0 border-[#aaa] mb-1 flex-[1]"></input>
              <button onClick={() => addSession()} className="bg-gray-200 hover:bg-gray-100 active:bg-gray-300 px-2 ml-1 h-[1.5rem]">Add</button>
            </span>
          ): null}
          {state?.sessions?.map((id: string) => <SessionText id={id} unsubmitted={false} key={id}/>)}
          {state.newSessionName ? <SessionText id={state.newSessionName} unsubmitted={true}/> : null}
          {(state.sessions == null || state.sessions.length === 0) && state.newSessionName == null ? <p>No sessions yet.</p> : null}
        </div>
        <div className="pt-2 md:pt-0 sm:px-5 min-h-screen flex-[1] bg-white drop-shadow-lg z-10">
          {state.sessions == null ? (
            <p className="m-5">Loading...</p>
          ) : (
            <div className="m-5 md:w-xl md:mx-auto">
              <CopilotChat
                disableSystemMessage={true}
                labels={{
                  title: "Advanced Analytics Agent",
                  initial: "Hi, there! You're chatting with the Advanced Analytics agent.",
                }}
                suggestions={[
                  {
                    title: "Patron count",
                    message: "How many current patrons are there?",
                  },
                  {
                    title: "What can you do",
                    message: "What sort of things can you do?",
                  },
                ]}
              />
            </div>
          )}
        </div>
      </div>
    </Main>
  );
}

export default function CopilotKitPage() {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="my_agent">
      <PageContent/>
    </CopilotKit>
  );
}
