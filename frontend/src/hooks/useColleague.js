/**
 * useColleague — Custom React hook that bridges a React component to the
 * Mediator pattern.
 *
 * On mount:   Creates a ConcreteColleague adapter, registers it with the mediator.
 * On unmount: Unregisters the colleague so stale references are cleaned up.
 *
 * Returns { send } so the component can fire events through the mediator.
 *
 * @param {string}   name            - Unique colleague name (e.g. "NotificationBell")
 * @param {function} receiveHandler  - Callback invoked when an event is routed to this colleague
 * @returns {{ send: (event: string, data?: any) => void }}
 */
import { useEffect, useRef, useCallback } from 'react';
import { useMediator } from '../context/MediatorContext';
import { Colleague } from '../patterns/mediator';

/**
 * ComponentColleague — a ConcreteColleague that adapts a React component.
 * Its receive() method delegates to the handler function provided by the hook.
 */
class ComponentColleague extends Colleague {
  constructor(name, mediator, handler) {
    super(name, mediator);
    this._handler = handler;
  }

  receive(event, data) {
    this._handler(event, data);
  }
}

export function useColleague(name, receiveHandler) {
  const mediator = useMediator();
  // Keep the handler ref up-to-date without re-registering
  const handlerRef = useRef(receiveHandler);
  handlerRef.current = receiveHandler;

  // Stable colleague instance across renders
  const colleagueRef = useRef(null);

  useEffect(() => {
    // Create a concrete colleague that delegates receive() to the current handler
    const colleague = new ComponentColleague(
      name,
      mediator,
      (event, data) => handlerRef.current(event, data),
    );
    colleagueRef.current = colleague;
    mediator.register(colleague);

    return () => {
      mediator.unregister(name);
      colleagueRef.current = null;
    };
  }, [name, mediator]);

  // Stable send function
  const send = useCallback(
    (event, data) => {
      if (colleagueRef.current) {
        colleagueRef.current.send(event, data);
      }
    },
    [],
  );

  return { send };
}
