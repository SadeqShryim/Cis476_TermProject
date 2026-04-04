/**
 * MediatorContext — provides the singleton DriveShareMediator instance
 * to the React component tree.
 *
 * This context does NOT perform mediation itself — it simply makes the
 * mediator instance accessible via useContext so that the useColleague
 * hook can register/unregister components.
 */
import { createContext, useRef, useContext } from 'react';
import { DriveShareMediator } from '../patterns/mediator';

const MediatorContext = createContext(null);

export function MediatorProvider({ children }) {
  // useRef guarantees a single mediator instance for the app lifetime
  const mediatorRef = useRef(new DriveShareMediator());

  return (
    <MediatorContext.Provider value={mediatorRef.current}>
      {children}
    </MediatorContext.Provider>
  );
}

export function useMediator() {
  const mediator = useContext(MediatorContext);
  if (!mediator) throw new Error('useMediator must be used within MediatorProvider');
  return mediator;
}
