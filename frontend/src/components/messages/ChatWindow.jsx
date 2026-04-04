/**
 * ChatWindow — message thread with input for sending messages.
 *
 * Mediator Role: ConcreteColleague ("ChatWindow")
 * Sends: MESSAGE_SENT
 */
import { useState, useEffect, useCallback, useRef } from 'react';
import { Send } from 'lucide-react';
import { useColleague } from '../../hooks/useColleague';
import { EVENTS } from '../../patterns/mediator';
import { useAuth } from '../../context/AuthContext';
import * as api from '../../api/client';

export default function ChatWindow({ partnerId }) {
  const { user } = useAuth();
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  const bottomRef = useRef(null);

  const fetchMessages = useCallback(async () => {
    if (!partnerId) return;
    const { ok, data } = await api.get(`/user/messages/${partnerId}`);
    if (ok) setMessages(data);
  }, [partnerId]);

  const { send } = useColleague('ChatWindow', (event) => {
    if (event === EVENTS.MESSAGE_SENT) fetchMessages();
  });

  useEffect(() => { fetchMessages(); }, [fetchMessages]);
  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: 'smooth' }); }, [messages]);

  async function handleSend(e) {
    e.preventDefault();
    if (!text.trim()) return;
    setSending(true);
    const { ok } = await api.post('/user/messages', {
      receiver_id: partnerId,
      content: text.trim(),
    });
    setSending(false);
    if (ok) {
      setText('');
      send(EVENTS.MESSAGE_SENT, { partnerId });
      fetchMessages();
    }
  }

  if (!partnerId) {
    return (
      <div className="flex-1 flex items-center justify-center text-gray-400 text-sm">
        Select a conversation to start messaging
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {messages.map(m => (
          <div key={m.id} className={`flex ${m.sender_id === user?.id ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[70%] px-3 py-2 rounded-lg text-sm
              ${m.sender_id === user?.id
                ? 'bg-purple-600 text-white'
                : 'bg-gray-100 text-gray-800'}`}>
              <p>{m.content}</p>
              <p className={`text-xs mt-1 ${m.sender_id === user?.id ? 'text-purple-200' : 'text-gray-400'}`}>
                {new Date(m.timestamp).toLocaleTimeString()}
              </p>
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSend} className="p-4 border-t border-gray-200 flex gap-2">
        <input type="text" value={text} onChange={e => setText(e.target.value)}
          placeholder="Type a message..."
          className="flex-1 px-3 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none" />
        <button type="submit" disabled={sending}
          className="p-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 disabled:opacity-50">
          <Send size={16} />
        </button>
      </form>
    </div>
  );
}
