/**
 * MessagesPage — two-column messaging layout with conversation list and chat window.
 */
import { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ConversationList from '../components/messages/ConversationList';
import ChatWindow from '../components/messages/ChatWindow';

export default function MessagesPage() {
  const { userId } = useParams();
  const navigate = useNavigate();
  const [selectedUserId, setSelectedUserId] = useState(userId || null);

  function handleSelect(partnerId) {
    setSelectedUserId(partnerId);
    navigate(`/dashboard/messages/${partnerId}`, { replace: true });
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-900 mb-4">Messages</h1>
      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden flex" style={{ height: '500px' }}>
        <div className="w-72 flex-shrink-0">
          <ConversationList selectedUserId={selectedUserId} onSelect={handleSelect} />
        </div>
        <ChatWindow partnerId={selectedUserId} />
      </div>
    </div>
  );
}
