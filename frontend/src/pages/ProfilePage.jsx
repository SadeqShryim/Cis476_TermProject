/**
 * ProfilePage — user profile displaying email, balance, and member since date.
 * Also shows reviews received by the user.
 */
import { useState, useEffect } from 'react';
import { User, Wallet, Calendar } from 'lucide-react';
import * as api from '../api/client';
import { useAuth } from '../context/AuthContext';
import ReviewList from '../components/reviews/ReviewList';
import LoadingSpinner from '../components/shared/LoadingSpinner';

export default function ProfilePage() {
  const { user } = useAuth();
  const [profile, setProfile] = useState(null);
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [profileRes, reviewsRes] = await Promise.all([
        api.get('/user/profile'),
        api.get(`/reviews/user/${user?.id}`),
      ]);
      if (profileRes.ok) setProfile(profileRes.data);
      if (reviewsRes.ok) setReviews(Array.isArray(reviewsRes.data) ? reviewsRes.data : reviewsRes.data.reviews ?? []);
      setLoading(false);
    }
    load();
  }, [user]);

  if (loading) return <LoadingSpinner />;

  return (
    <div className="max-w-2xl">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Profile</h1>

      {profile && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 mb-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="w-14 h-14 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center">
              <User size={28} />
            </div>
            <div>
              <h2 className="text-lg font-semibold text-gray-900">{profile.email}</h2>
              <p className="text-sm text-gray-500">Member since {new Date(profile.created_at).toLocaleDateString()}</p>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              <Wallet size={18} className="text-green-600" />
              <div>
                <p className="text-xs text-gray-500">Balance</p>
                <p className="text-lg font-bold text-gray-900">${profile.balance?.toFixed(2)}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg">
              <Calendar size={18} className="text-purple-600" />
              <div>
                <p className="text-xs text-gray-500">User ID</p>
                <p className="text-xs text-gray-700 font-mono truncate">{profile.id}</p>
              </div>
            </div>
          </div>
        </div>
      )}

      <h2 className="text-lg font-bold text-gray-900 mb-3">Reviews About You</h2>
      <ReviewList reviews={reviews} />
    </div>
  );
}
