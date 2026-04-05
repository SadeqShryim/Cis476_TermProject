/**
 * ConversationList — left panel showing all conversations.
 *
 * Mediator Role: ConcreteColleague ("ConversationList")
 * Listens for: MESSAGE_SENT — refreshes conversation list
 */
import { useState, useEffect, useCallback } from 'react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import * as api from '../../api/client';
import { MessageSquare } from 'lucide-react';

export default function ConversationList({ selectedUserId, onSelect }) {
  const [conversations, setConversations] = useState([]);

  const fetchConversations = useCallback(async () => {
    const { ok, data } = await api.get('/user/messages');
    if (ok) setConversations(data);
  }, []);

  useColleague('ConversationList', (event) => {
    if (event === EVENTS.MESSAGE_SENT || event === EVENTS.USER_LOGGED_IN) {
      fetchConversations();
    }
  });

  useEffect(() => { fetchConversations(); }, [fetchConversations]);

  return (
    <div className="border-r border-gray-200 h-full overflow-y-auto">
      <div className="p-4 border-b border-gray-100">
        <h3 className="font-semibold text-gray-900 flex items-center gap-2">
          <MessageSquare size={16} /> Conversations
        </h3>
      </div>
      {conversations.length === 0 ? (
        <p className="p-4 text-sm text-gray-500">No conversations yet.</p>
      ) : (
        conversations.map(c => (
          <button key={c.partner_id} onClick={() => onSelect(c.partner_id)}
            className={`w-full text-left p-4 border-b border-gray-50 hover:bg-gray-50 transition-colors
              ${selectedUserId === c.partner_id ? 'bg-purple-50' : ''}`}>
            <div className="flex justify-between items-center">
              <span className="text-sm font-medium text-gray-900">{c.partner_email || c.partner_id}</span>
              {c.unread_count > 0 && (
                <span className="bg-purple-600 text-white text-xs w-5 h-5 flex items-center justify-center rounded-full">
                  {c.unread_count}
                </span>
              )}
            </div>
            {c.last_message && (
              <p className="text-xs text-gray-500 mt-1 truncate">{typeof c.last_message === 'string' ? c.last_message : c.last_message.content}</p>
            )}
          </button>
        ))
      )}
    </div>
  );
}
