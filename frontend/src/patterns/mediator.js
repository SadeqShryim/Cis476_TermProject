/**
 * ============================================================================
 *  MEDIATOR DESIGN PATTERN — DriveShare UI Component Communication
 * ============================================================================
 *
 *  Pattern:  Mediator (GoF Behavioral Pattern)
 *  Purpose:  Manage communication between different UI components, creating
 *            a cohesive and user-friendly interface. Components (Colleagues)
 *            do not reference each other directly — they communicate
 *            exclusively through the Mediator, which routes events to the
 *            appropriate recipients.
 *
 *  GoF Roles:
 *    Mediator  (abstract)       →  Defines the notify/register interface
 *    ConcreteMediator           →  DriveShareMediator — routes events between colleagues
 *    Colleague (abstract base)  →  Defines send/receive interface for participants
 *    ConcreteColleague          →  Each UI component that registers with the mediator
 *                                  (NotificationBell, BalanceDisplay, CarList, etc.)
 *
 *  How it works:
 *    1. Each participating UI component creates a Colleague and registers it
 *       with the DriveShareMediator on mount.
 *    2. When a component needs to inform others of a state change (e.g., a
 *       booking was created), it calls colleague.send(EVENT, data).
 *    3. The DriveShareMediator receives the event and uses its routing table
 *       to determine which other colleagues should be notified.
 *    4. Each recipient colleague's receive() method is called, allowing the
 *       corresponding UI component to react (e.g., refresh notifications).
 *    5. When a component unmounts, its colleague is unregistered.
 *
 *  This is NOT just React context/state management rebranded — the Mediator
 *  class maintains its own colleague registry and routing logic independent
 *  of the React component tree.
 * ============================================================================
 */

// ---------------------------------------------------------------------------
//  Event Constants — all events that flow through the mediator
// ---------------------------------------------------------------------------
export const EVENTS = {
  BOOKING_CREATED:    'BOOKING_CREATED',
  BOOKING_CANCELLED:  'BOOKING_CANCELLED',
  PAYMENT_PROCESSED:  'PAYMENT_PROCESSED',
  CAR_LISTED:         'CAR_LISTED',
  CAR_UPDATED:        'CAR_UPDATED',
  CAR_DELETED:        'CAR_DELETED',
  MESSAGE_SENT:       'MESSAGE_SENT',
  REVIEW_SUBMITTED:   'REVIEW_SUBMITTED',
  NOTIFICATIONS_READ: 'NOTIFICATIONS_READ',
  CAR_WATCHED:        'CAR_WATCHED',
  CAR_UNWATCHED:      'CAR_UNWATCHED',
  USER_LOGGED_IN:     'USER_LOGGED_IN',
  USER_LOGGED_OUT:    'USER_LOGGED_OUT',
};

// ---------------------------------------------------------------------------
//  Colleague (Abstract Base Class)
// ---------------------------------------------------------------------------
/**
 * Colleague — the abstract base for every UI component that participates
 * in mediated communication.
 *
 * Each Colleague has a unique name, a reference to the Mediator, and two
 * core methods:
 *   send(event, data)    — delegate an event to the Mediator for routing
 *   receive(event, data) — handle an incoming event (overridden per component)
 */
export class Colleague {
  /**
   * @param {string} name - Unique identifier for this colleague
   * @param {DriveShareMediator} mediator - The mediator instance
   */
  constructor(name, mediator) {
    if (new.target === Colleague) {
      throw new Error('Colleague is abstract and cannot be instantiated directly.');
    }
    this.name = name;
    this.mediator = mediator;
  }

  /**
   * Send an event through the mediator to notify other colleagues.
   * @param {string} event - Event name (use EVENTS constants)
   * @param {*} data - Optional payload
   */
  send(event, data) {
    this.mediator.notify(this.name, event, data);
  }

  /**
   * Receive an event from the mediator.  Must be overridden by concrete colleagues.
   * @param {string} event - Event name
   * @param {*} data - Optional payload
   */
  receive(event, data) {
    throw new Error(`Colleague "${this.name}" must implement receive().`);
  }
}

// ---------------------------------------------------------------------------
//  Routing Table — maps each event to the colleague names that should receive it
// ---------------------------------------------------------------------------
const ROUTING_TABLE = {
  [EVENTS.BOOKING_CREATED]:    ['NotificationBell', 'BalanceDisplay', 'CarList', 'WatchList', 'BookingList'],
  [EVENTS.BOOKING_CANCELLED]:  ['NotificationBell', 'CarList', 'BookingList'],
  [EVENTS.PAYMENT_PROCESSED]:  ['BalanceDisplay', 'NotificationBell', 'BookingList'],
  [EVENTS.CAR_LISTED]:         ['CarList', 'NotificationBell'],
  [EVENTS.CAR_UPDATED]:        ['CarList', 'WatchList', 'NotificationBell'],
  [EVENTS.CAR_DELETED]:        ['CarList', 'WatchList'],
  [EVENTS.MESSAGE_SENT]:       ['NotificationBell', 'ConversationList'],
  [EVENTS.REVIEW_SUBMITTED]:   ['NotificationBell', 'BookingList'],
  [EVENTS.NOTIFICATIONS_READ]: ['NotificationBell'],
  [EVENTS.CAR_WATCHED]:        ['WatchList', 'NotificationBell'],
  [EVENTS.CAR_UNWATCHED]:      ['WatchList', 'CarList'],
  [EVENTS.USER_LOGGED_IN]:     ['NotificationBell', 'BalanceDisplay'],
  [EVENTS.USER_LOGGED_OUT]:    [],  // handled specially — broadcast to ALL
};

// ---------------------------------------------------------------------------
//  DriveShareMediator (ConcreteMediator)
// ---------------------------------------------------------------------------
/**
 * DriveShareMediator — the concrete mediator that coordinates communication
 * between all UI component colleagues.
 *
 * Responsibilities:
 *   1. Maintain a registry of active colleagues (Map keyed by name).
 *   2. Route events from the sender to the appropriate recipients using
 *      the routing table defined above.
 *   3. Handle the USER_LOGGED_OUT event specially by broadcasting to all
 *      registered colleagues so every component can clear its state.
 *   4. Silently skip recipients that are not currently registered (the
 *      component may not be mounted).
 */
export class DriveShareMediator {
  constructor() {
    /** @type {Map<string, Colleague>} — registry of active colleagues */
    this._colleagues = new Map();
    /** @type {Array} — event log for debugging / demo purposes */
    this._eventLog = [];
  }

  /**
   * Register a colleague with the mediator.
   * @param {Colleague} colleague - The colleague instance to register
   */
  register(colleague) {
    this._colleagues.set(colleague.name, colleague);
  }

  /**
   * Unregister a colleague (typically when the component unmounts).
   * @param {string} name - The colleague's unique name
   */
  unregister(name) {
    this._colleagues.delete(name);
  }

  /**
   * Core mediation logic — route an event from the sender to recipients.
   *
   * The routing table determines which colleagues receive each event.
   * USER_LOGGED_OUT is a special case: it is broadcast to ALL registered
   * colleagues so every component can reset.
   *
   * @param {string} senderName - Name of the colleague that fired the event
   * @param {string} event      - Event name (from EVENTS constants)
   * @param {*}      data       - Optional payload
   */
  notify(senderName, event, data) {
    // Log the event for debugging / pattern demonstration
    this._eventLog.push({
      timestamp: new Date().toISOString(),
      sender: senderName,
      event,
      data,
    });

    // Special case: logout broadcasts to every registered colleague
    if (event === EVENTS.USER_LOGGED_OUT) {
      for (const [name, colleague] of this._colleagues) {
        if (name !== senderName) {
          colleague.receive(event, data);
        }
      }
      return;
    }

    // Normal routing: look up recipients from the routing table
    const recipients = ROUTING_TABLE[event] || [];
    for (const recipientName of recipients) {
      // Skip the sender (don't notify yourself) and skip unmounted colleagues
      if (recipientName === senderName) continue;
      const colleague = this._colleagues.get(recipientName);
      if (colleague) {
        colleague.receive(event, data);
      }
    }
  }

  /**
   * Return the event log (useful for debugging or demonstrating the pattern).
   * @returns {Array}
   */
  getEventLog() {
    return [...this._eventLog];
  }
}
