/**
 * ReviewList — displays a list of reviews for a user.
 */
import { Star } from 'lucide-react';

export default function ReviewList({ reviews }) {
  if (!reviews || reviews.length === 0) {
    return <p className="text-sm text-gray-500">No reviews yet.</p>;
  }

  return (
    <div className="space-y-3">
      {reviews.map(r => (
        <div key={r.id} className="p-4 bg-white border border-gray-200 rounded-lg">
          <div className="flex items-center gap-1 mb-1">
            {[1, 2, 3, 4, 5].map(s => (
              <Star key={s} size={14}
                className={s <= r.rating ? 'fill-yellow-400 text-yellow-400' : 'text-gray-300'} />
            ))}
            <span className="text-xs text-gray-400 ml-2">
              {new Date(r.created_at).toLocaleDateString()}
            </span>
          </div>
          {r.comment && <p className="text-sm text-gray-700">{r.comment}</p>}
          <p className="text-xs text-gray-400 mt-1">
            Reviewed as: {r.reviewed_role}
          </p>
        </div>
      ))}
    </div>
  );
}
