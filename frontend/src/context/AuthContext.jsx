/**
 * AuthContext — manages authentication state (user, token) and exposes
 * login / logout helpers to the component tree.
 *
 * On login/logout the context fires mediator events so that other
 * colleagues (NotificationBell, BalanceDisplay, etc.) can react.
 */
import { createContext, useContext, useState, useEffect, useRef, useCallback } from 'react';
import { useMediator } from './MediatorContext';
import { Colleague, EVENTS } from '../patterns/mediator';
import * as api from '../api/client';

const AuthContext = createContext(null);

/**
 * AuthColleague — ConcreteColleague that lets AuthContext send events
 * (USER_LOGGED_IN, USER_LOGGED_OUT) through the mediator.
 */
class AuthColleague extends Colleague {
  receive() { /* AuthContext only sends, never receives */ }
}

export function AuthProvider({ children }) {
  const mediator = useMediator();

  // Stable colleague for the lifetime of the provider
  const colleagueRef = useRef(null);
  if (!colleagueRef.current) {
    colleagueRef.current = new AuthColleague('Auth', mediator);
    mediator.register(colleagueRef.current);
  }

  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem('user');
    return stored ? JSON.parse(stored) : null;
  });

  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  // Fire USER_LOGGED_IN on first mount if already authenticated
  useEffect(() => {
    if (user && token) {
      colleagueRef.current.send(EVENTS.USER_LOGGED_IN, { user });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const login = useCallback((userData, authToken) => {
    setUser(userData);
    setToken(authToken);
    localStorage.setItem('user', JSON.stringify(userData));
    localStorage.setItem('token', authToken);
    colleagueRef.current.send(EVENTS.USER_LOGGED_IN, { user: userData });
  }, []);

  const logout = useCallback(async () => {
    colleagueRef.current.send(EVENTS.USER_LOGGED_OUT, {});
    await api.post('/auth/logout');
    setUser(null);
    setToken(null);
    localStorage.removeItem('user');
    localStorage.removeItem('token');
  }, []);

  return (
    <AuthContext.Provider value={{ user, token, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}
